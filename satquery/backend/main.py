
import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np

# This is the exact variable Uvicorn is looking for!
app = FastAPI(title="SatQuery AI - SIH26167")

# Allows your future frontend interface to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Folder where uploaded satellite pictures will be kept
UPLOAD_DIR = "uploaded_sat_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}

def validate_and_process_image(file_path: str):
    """
    Stage 1: Preprocessing.
    Opens the image and reads its structural data (width, height, format).
    """
    try:
        with Image.open(file_path) as img:
            width, height = img.size
            format_ = img.format
            img_array = np.array(img)
            channels = img_array.shape if len(img_array.shape) == 3 else 1

            return {
                "dimensions": f"{width}x{height}",
                "format": format_,
                "channels": channels
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid or corrupted image: {str(e)}")

def dummy_query_router(query: str):
    """
    Stage 2: Query Router.
    Scans the text question to pick the right satellite analysis workflow.
    """
    query_lower = query.lower()

    if any(k in query_lower for k in ["count", "detect", "find", "object", "ship", "building"]):
        return "Object Detection"
    elif any(k in query_lower for k in ["show", "crop", "forest", "segment", "area", "agriculture"]):
        return "Semantic Segmentation (Land Cover Classification)"
    elif any(k in query_lower for k in ["change", "before", "after", "damage", "compare"]):
        return "Multitemporal Change Detection"
    else:
        return "Visual Question Answering (VQA)"

@app.get("/")
def home():
    return {
        "project": "SatQuery AI",
        "sih_id": "sih26167",
        "status": "active",
        "stage": "1 & 2 Operational"
    }

@app.post("/analyze")
async def analyze_satellite_image(
    file: UploadFile = File(...),
    query: str = Form(...)
):
    # 1. Check file extension
    file_ext = os.path.splitext(file.filename).lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format {file_ext}. Use PNG, JPG, or TIFF."
        )

    # 2. Save image file to local folder
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 3. Read image dimensions and metadata
    metadata = validate_and_process_image(file_path)

    # 4. Route text query to find the correct task
    routed_task = dummy_query_router(query)

    # 5. Return JSON payload back to the user
    return {
        "status": "Success",
        "file_name": file.filename,
        "metadata": metadata,
        "user_query": query,
        "routed_to_task": routed_task,
        "message": f"Successfully parsed. Ready for {routed_task} processing."
    }
