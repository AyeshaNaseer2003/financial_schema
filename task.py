from spire.pdf.common import *
from spire.pdf import *
from dotenv import load_dotenv
import os
import json
from models import FinancialReport  # Your Pydantic schema
from google import generativeai as genai


# === Configuration ===
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)


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

# === 2. Save raw extracted text to a file (optional for debugging) ===
def save_text_to_file(text, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

# === 3. Load text from a file (optional for re-use) ===
def load_text_from_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

# === 4. Gemini structured output with schema binding ===
def query_gemini_structured_json(text_block):
    # Combine your system prompt and the text_block into a single user message
    PROMPT = """
You are a financial report parsing expert.
Given a financial report in plain text, extract structured financial data and output it as a JSON with the following schema:

{
  "title": "Financials",
  "company": {
    "name": "<CompanyName>",
    "financials": [
      {
        "year": <int>,
        "income_statement": { ... },
        "balance_sheet": { ... },
        "cash_flow": { ... }
      }
    ]
  }
}

Only return a valid JSON structure. Use null where values are missing. Match keys exactly as described.

Here is the financial report text:

""" + text_block

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(
        [
            {"role": "user", "parts": [PROMPT]},
        ]
    )

    raw_json = response.text.strip().strip("```json").strip("```")
    return raw_json


# === Run the full workflow ===
pdf_file = "ASTRA_ZENECA 2022-2024.pdf"
text_file = "parsed_text.txt"
json_file = "structured_output.json"

# Step 1 & 2
text = extract_text_from_pdf(pdf_file)
save_text_to_file(text, text_file)

# Step 3 & 4
text_data = load_text_from_file(text_file)
structured = query_gemini_structured_json(text_data)

# Save structured output
with open(json_file, "w", encoding="utf-8") as f:
    f.write(structured)

print("PDF parsed and structured JSON saved to:", json_file)


# Validate with Pydantic model
try:
    data_dict = json.loads(structured)
    report = FinancialReport(**data_dict)
    print("JSON is valid and matches the schema.")
except Exception as e:
    print("JSON validation failed:", e)