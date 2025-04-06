import pdfplumber
import os

def extract_text_from_pdf(file_path: str):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
            text += "\n\n"

    return text

def extract_all_pdfs(pdf_folder: str, output_folder: str):
    os.makedirs(output_folder, exist_ok=True)
    
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            path = os.path.join(pdf_folder, filename)
            output_path = os.path.join(output_folder, f"{filename}.txt")
            
            print(f"Processing: {filename}")
            content = extract_text_from_pdf(path)
            
            with open(output_path, "w") as f:
                f.write(content)

if __name__ == "__main__":
    extract_all_pdfs("../data/insurance_files", "../data/texts")
