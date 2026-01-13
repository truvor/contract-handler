from io import BytesIO
from typing import Literal

import dropbox
from dropbox import files
from pydantic.types import FilePath
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

from config import settings


def iter_file(file_path: FilePath, chunk_size=1024 * 1024):
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            yield chunk


def generate_license_pdf(
    license_id: str, legal_name: str, storage: Literal["local", "dbx"] = "local"
) -> bytes:
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


def upload_pdf_to_dbx(pdf_bytes: bytes, license_id: str) -> None:
    dbx = dropbox.Dropbox(settings.DROPBOX_TOKEN)
    FILE_PATH = f"/{license_id}.pdf"
    dbx.files_upload(pdf_bytes, FILE_PATH, mode=files.WriteMode.overwrite)

    shared_link = dbx.sharing_create_shared_link(FILE_PATH)
    return shared_link.url.replace("&dl=0", "&dl=1")
