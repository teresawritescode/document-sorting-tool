# document-sorting-tool

A lightweight Python tool to organize and analyze document archives (PDF, JPG, PNG). Designed for researchers, civil servants, and digital humanities projects dealing with political or administrative texts.

## Goal
Help researchers, students, and public sector professionals structure and manage archives of reports, position papers, scanned documents, and official files systematically.

## Features
- Processes PDFs and image files (JPG, PNG)
- Logs results to an Excel file for analysis
- Automatically sorts files into folders by keyword presence
- Retains folder structures for grouped scans

## Installation and Requirements
- Python 3.10+ installed
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed
- [Poppler](https://blog.alivate.com.au/poppler-windows/) installed and added to PATH
- Git recommended for cloning the repository
- Install dependencies using pip install -r requirements.txt

### Setup
```bash
git clone https://github.com/yourusername/document-sorting-tool.git
cd document-sorting-tool
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux
pip install pytesseract pdf2image pandas openpyxl PyPDF2 pillow
```

## How to Use
1. Place your PDFs and image files in the `source` folder.
2. Run the script:
```bash
python main.py
```
3. Processed files will sort into `processed/with_keywords` and `processed/without_keywords`.
4. Results will export to `document_analysis_log.xlsx` for review and filtering.

## Configuration

Before running, **adapt `config.py` to your needs**:
- **KEYWORDS**: Define your own keywords for searching in documents.
- **OCR_PAGES**: Set a page limit for OCR (e.g., `20` for first 20 pages) or `None` to process all pages.
- **TESSERACT_CMD and POPPLER_PATH**: Adjust to your system installation paths.
- **AUTO_RENAME**: Set to `True` if you want files renamed based on found keywords, `False` otherwise.
- **WINDOW**: Adjust how many words before and after a keyword to extract for context.
- **EXPORT_XLSX_NAME**: Change the output Excel filename if needed for project organization.

## Credits
- Python
- pytesseract + Tesseract OCR
- pdf2image
- pandas
- PyPDF2
- Poppler
- ChatGPT (OpenAI) for workflow assistance

## License
MIT License © 2025 Teresa Werner
