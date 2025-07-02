from spire.pdf.common import *
from spire.pdf import *
import os

# === 1. Extract text from PDF ===
def extract_text_from_pdf(file_path):
    doc = PdfDocument()
    doc.LoadFromFile(file_path)
    full_text = ""
    for i in range(doc.Pages.Count):
        page = doc.Pages.get_Item(i)
        extractor = PdfTextExtractor(page)
        options = PdfTextExtractOptions()
        full_text += extractor.ExtractText(options) + "\n\n"
    doc.Close()
    return full_text

# === 2. Save raw extracted text (optional) ===
def save_text_to_file(text, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

if __name__ == "__main__":
    pdf_file = "ASTRA_ZENECA 2022-2024.pdf"
    text_file = "parsed_text.txt"

    # Step 1: Extract and save PDF text
    extracted_text = extract_text_from_pdf(pdf_file)
    save_text_to_file(extracted_text, text_file)
    print("✅ PDF text extracted and saved to:", text_file)
