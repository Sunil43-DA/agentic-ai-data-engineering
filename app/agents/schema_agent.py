import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.tools.schema_tool import analyse_schema


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)


def run_schema_agent(file_path: str):

    # Step 1: Use the schema tool
    profile = analyse_schema(file_path)

    # Step 2: Convert the profile into readable JSON
    profile_json = json.dumps(profile, indent=2)

    # Step 3: Ask the LLM to interpret the profile
    prompt = f"""
You are a Data Engineering Agent.

Analyse the following dataset profile.

Identify:
1. Important schema information
2. Missing-value issues
3. Duplicate records
4. Potential data-quality concerns
5. Recommended next data-engineering actions

Dataset profile:

{profile_json}

Provide a clear and concise data-engineering analysis.
"""

    # Step 4: Send the profile to the LLM
    response = client.responses.create(
        model="openai/gpt-oss-20b",
        input=prompt
    )

    return response.output_text


if __name__ == "__main__":

    result = run_schema_agent("data/raw/customer.csv")

    print("\n===== AI DATA ENGINEERING ANALYSIS =====")
    print(result)