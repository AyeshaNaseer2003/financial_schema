from spire.pdf.common import *
from spire.pdf import *
from dotenv import load_dotenv
import os
import json
from models import FinancialReport  
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# === 0. Load environment ===
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

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

# === 3. Load text from a file ===
def load_text_from_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

# === 4. LangChain Gemini-2.0 Flash structured JSON generation ===
def extract_structured_json_from_text(text_block):
    # Gemini LLM via LangChain
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=API_KEY,
        temperature=0,
    )

    # Prompt template with schema string + report text
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a financial report parsing expert."),
        ("user", """
Extract structured financial data for years 2023 and 2024 from the following financial report.

Follow this Pydantic schema strictly:

```json
{schema}
Use null for missing values.

Match field names exactly.

Return only valid JSON, no explanations.

Report:
{text}
""")
])
    #  Output parser linked to your actual Pydantic schema
    parser = JsonOutputParser(pydantic_object=FinancialReport)

    #  Create LangChain pipeline
    chain = prompt | llm | parser

    #  Run the chain
    return chain.invoke({
        "schema": FinancialReport.schema_json(indent=2),
        "text": text_block
    })

pdf_file = "ASTRA_ZENECA 2022-2024.pdf"
text_file = "parsed_text.txt"
json_file = "structured_output.json"

# Step 1: Extract and save PDF text
extracted_text = extract_text_from_pdf(pdf_file)
save_text_to_file(extracted_text, text_file)

# Step 2: Load and send to Gemini
text_data = load_text_from_file(text_file)
try:
    structured_output = extract_structured_json_from_text(text_data)
except Exception as e:
    print("Gemini extraction failed:", e)
    exit(1)

# Step 3: Save structured JSON output (dict-safe)
if hasattr(structured_output, "dict"):
    json_data = structured_output.dict()
else:
    json_data = structured_output

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=2)


print("Structured JSON saved to:", json_file)

# Step 4: Validate (already parsed but double check)
try:
    report = FinancialReport(**json_data)
    print("JSON is valid and matches the schema.")
except Exception as e:
    print("JSON validation failed:", e)



