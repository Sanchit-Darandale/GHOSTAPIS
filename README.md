# QR Generator API

> A lightweight FastAPI service for generating clean QR code PNGs and hosting them with a single request.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## Overview

DS QR Generator API turns text, links, and other data into QR code images. Use `qr/qr/genqr` when you need the PNG directly, or `/qr/hostqr` when you want the generated image uploaded and returned as shareable links.

### Highlights

- PNG QR code generation with configurable output size
- Supports both GET query parameters and POST JSON bodies
- Output sizes clamped between `50` and `5000` pixels
- Optional upload flow with a concise JSON response
- Built-in rate limiting at 30 requests per minute per client address
- Interactive OpenAPI documentation through FastAPI

## Quick start

Requires Python 3.10 or newer.

```bash
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the development server:

```bash
uvicorn qr:app --reload
```

The API is available at <http://127.0.0.1:8000>. Explore the interactive documentation at <http://127.0.0.1:8000/docs>.

## API reference

### `GET` or `POST /qr/genqr`

Generates a QR code and returns a PNG image.

| Parameter | Required | Default | Description                                             |
| --------- | -------- | ------- | ------------------------------------------------------- |
| `data`    | Yes      | -       | Text or URL to encode.                                  |
| `size`    | No       | `512`   | Output width and height in pixels, from `50` to `5000`. |

#### GET

```bash
curl "http://127.0.0.1:8000/qr/genqr?data=https%3A%2F%2Fexample.com&size=800" --output qr.png
```

#### POST

```bash
curl -X POST "http://127.0.0.1:8000/qr/genqr" \
  -H "Content-Type: application/json" \
  -d '{"data":"https://example.com","size":800}' \
  --output qr.png
```

### `GET` or `POST /qr/hostqr`

Generates a QR code, uploads the PNG, and returns the upload service's shareable links.

#### GET

```bash
curl "http://127.0.0.1:8000/qr/hostqr?data=https%3A%2F%2Fexample.com&size=800"
```

#### POST

```bash
curl -X POST "http://127.0.0.1:8000/qr/hostqr" \
  -H "Content-Type: application/json" \
  -d '{"data":"https://example.com","size":800}'
```

Example response:

```json
{
  "success": true,
  "url": "https://dscloud.vercel.app/file/jCpCbvd8",
  "directlink": "https://dscloud.vercel.app/f/jCpCbvd8.png",
  "downloadlink": "https://dscloud.vercel.app/file/jCpCbvd8?dl",
  "type": "image/png",
  "uploadedAt": "2026-08-25 09:19:16"
}
```

The API exposes only these selected fields from the upload service response.

### `GET /`

Returns basic API information, endpoint paths, and the current rate limit.

## Configuration

The upload destination is defined by `UPLOAD_API` in `qr.py`:

```python
UPLOAD_API = "https://dscloud.vercel.app/api/upload"
```

## Project details

- **Author:** Sanchit Darandale
- **Repository:** <https://github.com/Sanchit-Darandale/GHOSTAPIS>
- **License:** MIT License
