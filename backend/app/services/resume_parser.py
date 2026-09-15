from io import BytesIO

from app.core.errors import ValidationError


SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf", ".docx"}
ALLOWED_MIME_TYPES = {
    ".txt": {"text/plain"},
    ".md": {"text/markdown", "text/plain"},
    ".pdf": {"application/pdf"},
    ".docx": {"application/vnd.openxmlformats-officedocument.wordprocessingml.document"},
}


def parse_resume_bytes(filename: str, content_type: str, data: bytes) -> str:
    suffix = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValidationError("Unsupported resume file type. Use TXT, MD, PDF, or DOCX.", {"code": "FILE_UNSUPPORTED"})
    if content_type and content_type != "application/octet-stream" and content_type not in ALLOWED_MIME_TYPES[suffix]:
        raise ValidationError("The file MIME type does not match its extension.", {"code": "FILE_MIME_MISMATCH"})
    if not data:
        raise ValidationError("The uploaded resume is empty.", {"code": "FILE_EMPTY"})

    try:
        if suffix in {".txt", ".md"}:
            return data.decode("utf-8", errors="replace").strip()
        if suffix == ".pdf":
            from pypdf import PdfReader

            return "\n\n".join((page.extract_text() or "") for page in PdfReader(BytesIO(data)).pages).strip()
        if suffix == ".docx":
            from docx import Document

            document = Document(BytesIO(data))
            return "\n".join(paragraph.text for paragraph in document.paragraphs).strip()
    except Exception as exc:
        raise ValidationError("The resume could not be parsed. Check that the file is not malformed or password-protected.", {"code": "FILE_PARSE_FAILED"}) from exc

    raise ValidationError("Unsupported resume file type.", {"code": "FILE_UNSUPPORTED"})