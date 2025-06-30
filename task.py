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


# === 4. Gemini structured output using actual Pydantic schema ===
def query_gemini_structured_json(text_block):
    schema_json = FinancialReport.schema_json(indent=2)

    prompt = f"""
You are a financial report parsing expert.

Your task is to extract structured financial data for years 2023 and 2024 from the plain text below.

You MUST return JSON that exactly follows this Pydantic schema:

```json
{schema_json}
Strict Instructions:

Match field names exactly (case-sensitive).

Do NOT change, omit, or invent any fields.

Use null for any missing or unavailable values.

Do NOT return explanations — only valid JSON output.

--- BEGIN FINANCIAL REPORT TEXT ---
{text_block}
--- END REPORT ---
"""
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(
        [{"role": "user", "parts": [prompt]}]
    )

    # Clean up markdown-style code block if present
    raw_json = response.text.strip()
    if raw_json.startswith("```json"):
        raw_json = raw_json.removeprefix("```json").removesuffix("```").strip()

    return raw_json


pdf_file = "ASTRA_ZENECA 2022-2024.pdf"
text_file = "parsed_text.txt"
json_file = "structured_output.json"

# Step 1: Extract and save PDF text
extracted_text = extract_text_from_pdf(pdf_file)
save_text_to_file(extracted_text, text_file)

# Step 2: Load text and query Gemini
text_data = load_text_from_file(text_file)
structured_json_string = query_gemini_structured_json(text_data)

# Step 3: Save structured output
with open(json_file, "w", encoding="utf-8") as f:
    f.write(structured_json_string)

print("✅ PDF parsed and structured JSON saved to:", json_file)

# Step 4: Validate with Pydantic model
try:
    data_dict = json.loads(structured_json_string)
    report = FinancialReport(**data_dict)
    print("✅ JSON is valid and matches the schema.")
except Exception as e:
    print("❌ JSON validation failed:", e)
