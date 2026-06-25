from pathlib import Path

from app.parsers.docx_parser import DocxParser
from app.parsers.pdf_parser import PDFParser


class ParserFactory:

    @staticmethod
    def extract_text(file_path: str):

        extension = Path(file_path).suffix.lower()

        if extension == ".docx":
            return DocxParser.extract_text(file_path)

        elif extension == ".pdf":
            return PDFParser.extract_text(file_path)

        else:
            raise Exception(f"Unsupported file type: {extension}")