import os
import json
from dotenv import load_dotenv
from langfuse import get_client
from langfuse.langchain import CallbackHandler
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from models import FinancialReport

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# 1 Load PDF-extracted text
def load_text_from_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

# 2 Setup Langfuse tracing + Prompt
langfuse = get_client()
langfuse_handler = CallbackHandler()

lf_prompt = langfuse.get_prompt("financial_prompt", label="production")
langchain_text = lf_prompt.get_langchain_prompt()
prompt = ChatPromptTemplate.from_template(langchain_text, metadata={"langfuse_prompt": lf_prompt})

# 3 Build Gemini + JSON parser pipeline
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=API_KEY, temperature=0)
parser = JsonOutputParser(pydantic_object=FinancialReport)
chain = prompt | llm | parser

# 4 Execute and save
if __name__ == "__main__":

    parsing_file= "parsed_text.txt"
    json_file="structured_output.json"

    text = load_text_from_file(parsing_file)

    try:
        result = chain.invoke(
            {"schema": json.dumps(FinancialReport.model_json_schema(), indent=2), "text": text},
            config={"callbacks": [langfuse_handler]}
        )
    except Exception as e:
        print("Extraction failed:", e)
        exit(1)

    data = result.dict() if hasattr(result, "dict") else result

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("Structured JSON saved")

    try:
        FinancialReport(**data)
        print("JSON validates against your schema")
    except Exception as e:
        print("Validation error:", e)
