from pathlib import Path

from docx import Document as DocxDocument
from pypdf import PdfReader


class TextExtractor:

    def extract_text(
        self,
        file_path: str,
    ) -> str:

        extension = Path(
            file_path
        ).suffix.lower()

        if extension == ".pdf":
            return self._extract_pdf(
                file_path
            )

        if extension == ".docx":
            return self._extract_docx(
                file_path
            )

        if extension == ".txt":
            return self._extract_txt(
                file_path
            )

        if extension == ".md":
            return self._extract_md(
                file_path
            )

        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    def _extract_pdf(
        self,
        file_path: str,
    ) -> str:

        reader = PdfReader(
            file_path
        )

        text = ""

        for page in reader.pages:

            page_text = (
                page.extract_text()
                or ""
            )

            text += page_text + "\n"

        return text.strip()

    def _extract_docx(
        self,
        file_path: str,
    ) -> str:

        document = DocxDocument(
            file_path
        )

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        ).strip()

    def _extract_txt(
        self,
        file_path: str,
    ) -> str:

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:

            return file.read().strip()

    def _extract_md(
        self,
        file_path: str,
    ) -> str:

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:

            return file.read().strip()