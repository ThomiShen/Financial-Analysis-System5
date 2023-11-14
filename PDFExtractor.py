import pytesseract
from pdf2image import convert_from_path

class PDFExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def _pdf_to_images(self):
        return convert_from_path(self.pdf_path)

    def extract_text(self):
        images = self._pdf_to_images()
        full_text = ""
        for image in images:
            text = pytesseract.image_to_string(image, lang='eng+chi_sim')
            full_text += text
        return full_text

# 使用示例
pdf_path = 'path_to_your_pdf_file.pdf'
extractor = PDFExtractor(pdf_path)
text = extractor.extract_text()

with open('output.txt', 'w', encoding='utf-8') as f:
    f.write(text)
