import os
import time
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests

VISITED_LOG = "logs/visited.txt"
TO_VISIT_LOG = "logs/to_visit.txt"
FAILED_LOG = "logs/failed.txt"
os.makedirs("logs", exist_ok=True)


def save_list_to_file(filepath, items):
    with open(filepath, "w") as f:
        f.write("\n".join(items))

def load_list_from_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

BASE_URL = "https://www.angelone.in/support"
SAVE_DIR = "data/web"

def is_valid_url(url):
    if not url.startswith(BASE_URL):
        return False
    if "/hindi/" in url:
        return False
    return True

def get_all_links(page_content, base_url):
    soup = BeautifulSoup(page_content, "html.parser")
    links = set()
    main_content = soup.find(class_="main-grid")
    for a_tag in main_content.find_all("a", href=True):
        href = urljoin(base_url, a_tag["href"])
        if is_valid_url(href):
            links.add(href.split("#")[0])  # Remove fragment
    return list(links)

def extract_text_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    main_content = soup.find(class_="main-grid")
    if not main_content:
        return ""  # or return fallback full text

    # Remove unnecessary tags
    for tag in main_content(["script", "style", "noscript"]):
        tag.decompose()

    return main_content.get_text(separator="\n", strip=True)

def scrape_support_pages():
    os.makedirs(SAVE_DIR, exist_ok=True)
    visited = load_list_from_file(VISITED_LOG)
    to_visit = load_list_from_file(TO_VISIT_LOG)
    if not to_visit:
        to_visit = set([BASE_URL])  # fresh start

    failed = load_list_from_file(FAILED_LOG)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        while to_visit:
            url = to_visit.pop()
            if url in visited:
                continue

            print(f"Visiting: {url}")
            try:
                page.goto(url, timeout=15000)
                page.wait_for_timeout(2000)
                html = page.content()

                # Save clean text
                text = extract_text_from_html(html)
                filename = urlparse(url).path.replace("/", "_").strip("_") + ".txt"
                with open(os.path.join(SAVE_DIR, filename), "w") as f:
                    f.write(text)

                visited.add(url)
                links = get_all_links(html, url)
                to_visit.update(set(links) - visited)

            except Exception as e:
                print(f"Failed: {url} — {e}")
            
            save_list_to_file(VISITED_LOG, visited)
            save_list_to_file(TO_VISIT_LOG, to_visit)
            save_list_to_file(FAILED_LOG, failed)

        browser.close()

if __name__ == "__main__":
    scrape_support_pages()
