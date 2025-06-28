# main.py

"""
document-sorting-tool

Processes PDFs and image files, extracts text using OCR, searches for keywords,
and organizes files into structured folders with an XLSX export for further analysis.
"""

import os
import re
import shutil
import pandas as pd
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import PyPDF2
from config import *

# Create required folders if they do not exist
folders = [SOURCE_FOLDER, WITH_KEYWORDS_FOLDER, WITHOUT_KEYWORDS_FOLDER]
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Extract metadata from PDFs
def extract_metadata(path):
    try:
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            info = reader.metadata
            title = info.title if info.title else "untitled"
            author = info.author if info.author else "unknown"
            date = info.get('/CreationDate')
            year = date[2:6] if date and date.startswith('D:') else "undated"
            return title, author, year
    except:
        return "untitled", "unknown", "undated"

# OCR for PDFs
def ocr_text_pdf(path):
    try:
        images = convert_from_path(path, poppler_path=POPPLER_PATH)
        text = ""
        for img in images[:OCR_PAGES] if OCR_PAGES else images:
            text += pytesseract.image_to_string(img, lang='deu+eng+fra+por') + "\n"
        return text
    except Exception as e:
        print(f"❌ OCR failed for PDF {path}: {e}")
        return None

# OCR for images
def ocr_text_image(path):
    try:
        img = Image.open(path)
        text = pytesseract.image_to_string(img, lang='deu+eng+fra+por')
        return text
    except Exception as e:
        print(f"❌ OCR failed for image {path}: {e}")
        return None

# Keyword and context extraction
def extract_keywords_and_context(text, keyword_list):
    found = {}
    contexts = []
    words = re.findall(r'\w+|\W+', text)
    for keyword in keyword_list:
        positions = [i for i, w in enumerate(words) if keyword.lower() in w.lower()]
        if positions:
            found[keyword] = len(positions)
            for pos in positions:
                start = max(0, pos - WINDOW)
                end = min(len(words), pos + WINDOW)
                context = ''.join(words[start:end]).replace('\n', ' ')
                contexts.append(context.strip())
    return found, contexts

# Collect all files to process with paths
files_to_process = []
for root, dirs, files in os.walk(SOURCE_FOLDER):
    for file in files:
        if file.lower().endswith((".pdf", ".jpg", ".jpeg", ".png")):
            files_to_process.append((root, file))

# Processing pipeline with simple progress indication
rows = []
total_files = len(files_to_process)

for idx, (root, file) in enumerate(files_to_process, 1):
    print(f"Processing file {idx} of {total_files}: {file}")
    path = os.path.join(root, file)
    folder_has_keyword = False
    is_root_source = os.path.abspath(root) == os.path.abspath(SOURCE_FOLDER)

    if file.lower().endswith(".pdf"):
        title, author, year = extract_metadata(path)
        text = ocr_text_pdf(path)
    else:
        title, author, year = "image", "unknown", "undated"
        text = ocr_text_image(path)

    if text is None:
        continue

    keyword_counts, contexts = extract_keywords_and_context(text, KEYWORDS)

    if keyword_counts and AUTO_RENAME:
        main_keyword = max(keyword_counts, key=keyword_counts.get).replace(" ", "-")
        new_name = f"{main_keyword}_{file}"
        os.rename(path, os.path.join(root, new_name))
        file = new_name

    row_data = {
        "Filename": file,
        "Folder": os.path.relpath(root, SOURCE_FOLDER),
        "Title": title,
        "Author": author,
        "Year": year,
        "Keywords_Found": str(keyword_counts),
        "Contexts": " | ".join(contexts[:5])
    }
    rows.append(row_data)

    # Move files appropriately
    target_base = WITH_KEYWORDS_FOLDER if keyword_counts else WITHOUT_KEYWORDS_FOLDER
    if is_root_source:
        src_file = os.path.join(SOURCE_FOLDER, file)
        target_path = os.path.join(target_base, file)
        shutil.move(src_file, target_path)
    else:
        rel_path = os.path.relpath(root, SOURCE_FOLDER)
        target_folder = os.path.join(target_base, rel_path)
        if not os.path.exists(os.path.dirname(target_folder)):
            os.makedirs(os.path.dirname(target_folder), exist_ok=True)
        shutil.move(root, target_folder)
        break  # Stop processing further in this folder after moving it

# Export results to XLSX
df = pd.DataFrame(rows)
df.to_excel(EXPORT_XLSX_NAME, index=False)
print(f"✅ Processing complete. Results saved to {EXPORT_XLSX_NAME}")
