from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.responses import StreamingResponse

from auth import verify_jwt
from utils import (
    generate_license_pdf,
    iter_file,
    stream_remote_audio,
    upload_pdf_to_dbx,
)

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="Vercel + FastAPI",
    description="Vercel + FastAPI",
    version="1.0.0",
)


@app.post("/purchase", dependencies=[Depends(verify_jwt)])
async def purchase_license():
    license_id = "34"
    pdf_bytes = generate_license_pdf(license_id, legal_name="John", storage="local")
    pdf_url = upload_pdf_to_dbx(pdf_bytes, license_id)
    return {"license_id": license_id, "pdf_url": pdf_url}


@app.get("/licenses/{license_id}/download", dependencies=[Depends(verify_jwt)])
def download_license(license_id: str):
    file_name = f"{license_id}.pdf"
    file_path = (BASE_DIR / file_name).resolve()

    return StreamingResponse(
        iter_file(file_path),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{license_id}.pdf"'},
    )


@app.get("/audio/{id}", dependencies=[Depends(verify_jwt)])
def download_mp3(id: str):
    file_url = (
        "https://bwstldmlrcsfzusnmcwq.supabase.co/storage/v1/object/public/mp3/GANG.mp3"
    )
    return StreamingResponse(
        stream_remote_audio(file_url),
        media_type="audio/mpeg",
        headers={"Content-Disposition": "inline"},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)
