from io import BytesIO
from pathlib import Path

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

BASE_DIR = Path.cwd()


def iter_file(path: str, chunk_size=1024 * 1024):
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            yield chunk


def generate_license_pdf(license_id: str, legal_name: str) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=LETTER)

    text = c.beginText(40, 750)
    text.textLine("BEAT LICENSE AGREEMENT")
    text.textLine("")
    text.textLine(f"Licensee: {legal_name}")
    text.textLine(f"License ID: {license_id}")
    text.textLine("")
    text.textLine("This agreement is executed electronically.")
    text.textLine(f"Accepted electronically by {legal_name}.")

    c.drawText(text)
    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer.read()


def upload_pdf(pdf_bytes: bytes, license_id: str) -> str:
    filename = f"{license_id}.pdf"
    file_path = BASE_DIR / filename

    with open(file_path, "wb") as f:
        f.write(pdf_bytes)

    return str(file_path)
