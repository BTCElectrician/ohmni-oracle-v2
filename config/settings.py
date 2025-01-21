import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Azure Document Intelligence Settings
DOCUMENTINTELLIGENCE_ENDPOINT = os.getenv("DOCUMENTINTELLIGENCE_ENDPOINT")
DOCUMENTINTELLIGENCE_KEY = os.getenv("DOCUMENTINTELLIGENCE_API_KEY")

# Processing Settings
MAX_FILE_SIZE = 50_000_000  # 50MB
SUPPORTED_FILE_TYPES = [".pdf"]

PANEL_SCHEDULE_PATTERNS = [
    "-PANEL-SCHEDULES-",
    "-ELECTRICAL-SCHEDULES-"
]