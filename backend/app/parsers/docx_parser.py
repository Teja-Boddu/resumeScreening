from docx import Document


class DocxParser:

    @staticmethod
    def extract_text(file_path: str) -> str:
        """
        Extract text from a DOCX resume.
        """

        document = Document(file_path)

        text = []

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                text.append(paragraph.text)

        return "\n".join(text)