from docx import Document
import os

def extract_text_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

def extract_all_docx(docx_folder: str, output_folder: str):
    os.makedirs(output_folder, exist_ok=True)
    
    for filename in os.listdir(docx_folder):
        if filename.endswith(".docx"):
            path = os.path.join(docx_folder, filename)
            output_path = os.path.join(output_folder, f"{filename}.txt")
            
            print(f"Processing: {filename}")
            content = extract_text_from_docx(path)
            
            with open(output_path, "w") as f:
                f.write(content)

if __name__ == "__main__":
    extract_all_docx("../data/insurance_files", "../data/texts")
