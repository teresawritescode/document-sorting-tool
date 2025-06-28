# config.py

# Folder paths
SOURCE_FOLDER = "source"
PROCESSED_FOLDER = "processed"
WITH_KEYWORDS_FOLDER = f"{PROCESSED_FOLDER}/with_keywords"
WITHOUT_KEYWORDS_FOLDER = f"{PROCESSED_FOLDER}/without_keywords"

# Keywords to search for
KEYWORDS = [
    "migration", "digitalisation", "frontex", "refugee", "foreign policy"
]

# OCR and processing settings
OCR_PAGES = None
WINDOW = 100
AUTO_RENAME = True
EXPORT_XLSX_NAME = "document_analysis_log.xlsx"

# Poppler and Tesseract paths (adjust as needed)
POPPLER_PATH = r"C:\Program Files (x86)\poppler-24.08.0\Library\bin"
TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
