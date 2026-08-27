import httpx
import qrcode
from io import BytesIO
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import Response
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler

app = FastAPI(title="DS QR Generator API")
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

UPLOAD_API = "https://dscloud.vercel.app/api/upload"

class QRRequest(BaseModel):
    data: str
    size: int = 512

def make_qr(data: str, size: int):
    size = max(50, min(size, 5000))

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    img = img.resize((size, size), resample=0)

    buf = BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()

@app.api_route("/qr/genqr", methods=["GET", "POST"])
@limiter.limit("30/minute")
async def genqr(
    request: Request,
    qr_request: QRRequest | None = None,
    data: str | None = None,
    size: int | None = None
):
    if data is not None:
        qr_data, qr_size = data, size or 512

    elif qr_request:
        qr_data, qr_size = qr_request.data, qr_request.size

    else:
        return {
            "Error": "data parameter is required",
            "Developer": "Sanchit"    
        }

    return Response(
        make_qr(qr_data, qr_size),
        media_type="image/png",
        headers={"Cache-Control": "public, max-age=3600"}
    )


@app.api_route("/qr/hostqr", methods=["GET", "POST"])
@limiter.limit("30/minute")
async def hostqr(
    request: Request,
    qr_request: QRRequest | None = None,
    data: str | None = None,
    size: int | None = None
):
    if data is not None:
        qr_data, qr_size = data, size or 512

    elif qr_request:
        qr_data, qr_size = qr_request.data, qr_request.size

    else:
        return {
            "Error": "data parameter is required",
            "Developer": "Sanchit"    
        }

    png = make_qr(qr_data, qr_size)

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            UPLOAD_API,
            files={"file": ("qr.png", png, "image/png")}
        )

    if r.status_code >= 400:
        return {
            "error": "QR hosting failed",
            "status": r.status_code,
            "details": r.text
        }

    upload_result = r.json()
    return {
        "success": upload_result.get("success"),
        "url": upload_result.get("url"),
        "directlink": upload_result.get("directlink"),
        "downloadlink": upload_result.get("downloadlink"),
        "type": upload_result.get("type"),
        "uploadedAt": upload_result.get("uploadedAt")
    }

@app.get("/qr")
def home():
    return {
        "api": "DS QR Generator API",
        "generate": "/qr/genqr?data={data}&size={size}",
        "host": "/qr/hostqr?data={data}&size={size}",
        "rate_limit": "30 requests/minute",
        "developer": "Sanchit"    
    }
