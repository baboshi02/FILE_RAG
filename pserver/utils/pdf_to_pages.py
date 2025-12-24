from pymupdf import Document
import unicodedata
import re


def clean_ocr_text(text):
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"-\s*\n\s*", "", text)
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = text.strip()
    return text


def pdf_to_pages(pdf: bytes):
    doc = Document(stream=pdf)
    markdown = []
    for page in doc:
        text = page.get_text("text")
        if not text.strip():  # type: ignore
            ocr = page.get_textpage_ocr(dpi=200)
            text = ocr.extractText()
            text = clean_ocr_text(text)
        markdown.append(text)
    return markdown
