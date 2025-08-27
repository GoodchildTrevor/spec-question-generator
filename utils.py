from collections.abc import Iterable
from logging import Logger
import os
from pathlib import Path
import re

import aspose.words as aw
from docx2python import docx2python
import fitz
from fitz import Document
import pytesseract
from PIL import Image

from config import (
    PDF_SIZE_LIMIT,
    DPI
)


def save_text_to_file(text: str, filename: str) -> None:
    """
    Saving text in particular file
    :param text: final text
    :param filename: name of txt file
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)


def normalize_text(text: str) -> str:
    """
    Normalizing raw text: removing spaces, unicode normalizing, punctuation unification
    :param  text: raw text
    :return: normalized doc's text
    """
    # Unicode normalizing
    text = unicodedata.normalize('NFKC', text)
    # Removing blank spaces
    text = re.sub(r'\s+', ' ', text)
    text = '\n'.join(line.strip() for line in text.split('\n'))
    # Normalizing punctuation
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace('–', '-').replace('—', '-')

    return text.strip()


def file_to_text(logger: Logger, file_path: Path, file_format: str) -> str:
    """
    Extracts textual content from a given file.
    :param logger: Logger instance for logging events.
    :param file_path: link of the document
    :param file_format: pdf/doc/djvu
    :return: document's text
    """
    text = ""
    if file_format == ".pdf":
        doc = fitz.open(file_path)
        text = pdf_to_text(doc)
        doc.close
    elif file_format in [".docx", ".doc"]:
        if file_format == ".doc":
            file_path = convert_doc_to_docx(file_path)
        with docx2python(file_path) as doc_result:
            all_parts = [
                doc_result.body,
                doc_result.header,
                doc_result.footer
            ]
        text = word_to_text(all_parts)
    else:
        logger.warning(f"Unsupported file format: {file_format}")
    return text


def pdf_to_text(doc: Document) -> str:
    """
    Extract pdf text: both if it contains text or image
    :param doc: pymupdf Document
    :return: text of document
    """
    full_text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_text = page.get_text()
        if len(page_text.strip()) < PDF_SIZE_LIMIT:
            pix = page.get_pixmap(dpi=DPI)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            page_text = pytesseract.image_to_string(img, lang='rus+eng')
        full_text += page_text + "\n"
    return full_text


def convert_doc_to_docx(file_path: Path) -> str:
    """
    Convert .doc extension to .docx extension
    :param file_path: link of the document
    :return: new path
    """
    new_path = os.path.splitext(file_path)[0] + ".docx"
    doc = aw.Document(file_path)
    doc.save(new_path)
    return new_path


def word_to_text(all_parts: list[list[list[list[list[str]]]]]) -> str:
    """
    Extract text form standard .doc and .docx files
    :param all_parts: list of word doc elements
    :return: text of document
    """
    text_items = []

    def extract_text_recursively(data: str | Iterable) -> None:
        """
        Recursively extracts text from nested structures.
        :param data: A string or an iterable containing strings or further nested iterables.
        """
        if isinstance(data, str):
            if data and data.strip():
                text_items.append(data.strip())
        elif isinstance(data, Iterable):
            for item in data:
                extract_text_recursively(item)

    for part in all_parts:
        extract_text_recursively(part)

    return '\n'.join(filter(None, text_items))
