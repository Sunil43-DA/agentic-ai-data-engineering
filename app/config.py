import os

from dotenv import load_dotenv


# ==================================================
# Load Environment Variables
# ==================================================

load_dotenv()


# ==================================================
# Groq Configuration
# ==================================================

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)

GROQ_BASE_URL = os.getenv(
    "GROQ_BASE_URL",
    "https://api.groq.com/openai/v1"
)

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)


# ==================================================
# Pipeline Configuration
# ==================================================

INPUT_FILE = os.getenv(
    "INPUT_FILE",
    "data/raw/customer.csv"
)

CLEANED_FILE = os.getenv(
    "CLEANED_FILE",
    "data/clean/customer_cleaned.csv"
)

MAX_RETRIES = int(
    os.getenv(
        "MAX_RETRIES",
        "2"
    )
)


# ==================================================
# Configuration Validation
# ==================================================

if not GROQ_API_KEY:

    raise ValueError(
        "GROQ_API_KEY is not configured. "
        "Please add it to the .env file."
    )