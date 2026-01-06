from fastapi import Depends, FastAPI
from fastapi.responses import StreamingResponse

from auth import verify_jwt
from utils import generate_license_pdf, iter_file, upload_pdf_to_dbx

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
    file_path = f"./{license_id}.pdf"

    return StreamingResponse(
        iter_file(file_path),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{license_id}.pdf"'},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)
