import fitz
from PIL import Image
import pytesseract
import numpy as np

def pdf_to_images(pdf_path):
    """Converts a PDF file into a list of images."""
    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    return images

def extract_text_from_images(image_list):
    """Extracts text from a list of images using Tesseract OCR."""
    texts = []
    for img in image_list:
        text = pytesseract.image_to_string(img)
        texts.append(text)
    return texts