import os
import pdfplumber
import camelot
import pytesseract

def ingest_document(pdf_path):
    """
    Ingest a PDF and extract:
    - Text by page
    - Tables by page
    - Images by page + OCR
    Returns a dictionary with 'text', 'tables', 'images'.
    """
    doc_data = {"text": [], "tables": [], "images": []}

    # ---------------- Text & Images ----------------
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            # Extract text
            text = page.extract_text()
            if text and text.strip():
                doc_data["text"].append({"page": i+1, "text": text})

            # Extract images with OCR
            try:
                for img in page.images:
                    # Crop image from page
                    x0, top, x1, bottom = img["x0"], img["top"], img["x1"], img["bottom"]
                    pil_img = page.to_image(resolution=300).original.crop((x0, top, x1, bottom))
                    ocr_text = pytesseract.image_to_string(pil_img)
                    if ocr_text.strip():
                        doc_data["images"].append({"page": i+1, "ocr_text": ocr_text})
            except Exception as e:
                print(f"Skipped image on page {i+1}: {e}")

    # ---------------- Tables ----------------
    # Camelot table extraction
    try:
        tables = camelot.read_pdf(pdf_path, pages='all', flavor='lattice')
        for t in tables:
            doc_data["tables"].append({"page": int(t.page), "table": t.df})
    except Exception as e:
        print(f"Table extraction failed: {e}")

    return doc_data
