from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

import os
import shutil


# --------------------------------------------------
# SATQUERY AI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="SatQuery AI",
    description="Interactive Vision-Language Assistant for Remote Sensing Image Analysis",
    version="1.0.0"
)


# --------------------------------------------------
# DIRECTORIES
# --------------------------------------------------

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


# --------------------------------------------------
# STATIC FILES
# --------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# --------------------------------------------------
# HTML TEMPLATES
# --------------------------------------------------

templates = Jinja2Templates(
    directory="templates"
)


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# --------------------------------------------------
# IMAGE ANALYSIS ENDPOINT
# --------------------------------------------------

@app.post("/analyze")
async def analyze(
    query: str = Form(...),
    image: UploadFile = File(...)
):

    # Create image path
    file_path = os.path.join(
        UPLOAD_DIR,
        image.filename
    )

    # Save uploaded image
    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            image.file,
            buffer
        )

    # Temporary response
    return {
        "status": "success",
        "query": query,
        "image": image.filename,
        "message": "Satellite image uploaded successfully."
    }
