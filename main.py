from fastapi import (
    FastAPI,
    File,
    UploadFile,
    Form,
    Request,
    HTTPException
)

from fastapi.responses import (
    HTMLResponse,
    FileResponse
)

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import os
import shutil


# ==========================================
# SATQUERY AI SERVICES
# ==========================================

from services.query_engine import (
    understand_query
)

from services.object_detector import (
    detect_objects
)

from services.vegetation_analyzer import (
    analyze_vegetation
)

from services.segmentation import (
    segment_image
)


# ==========================================
# BASE DIRECTORY
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(

    title="SatQuery AI",

    description=(
        "Interactive Vision-Language Assistant "
        "for Remote Sensing Image Analysis"
    ),

    version="1.0.0"
)


# ==========================================
# DIRECTORIES
# ==========================================

UPLOAD_DIR = os.path.join(
    BASE_DIR,
    "uploads"
)

RESULTS_DIR = os.path.join(
    BASE_DIR,
    "runs"
)


# ==========================================
# CREATE DIRECTORIES
# ==========================================

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

os.makedirs(
    RESULTS_DIR,
    exist_ok=True
)


# ==========================================
# STATIC FILES
# ==========================================

app.mount(

    "/static",

    StaticFiles(

        directory=os.path.join(
            BASE_DIR,
            "static"
        )

    ),

    name="static"
)


# ==========================================
# HTML TEMPLATES
# ==========================================

templates = Jinja2Templates(

    directory=os.path.join(
        BASE_DIR,
        "templates"
    )

)


# ==========================================
# HOME PAGE
# ==========================================

@app.get(
    "/",
    response_class=HTMLResponse
)

async def home(
    request: Request
):

    return templates.TemplateResponse(

        request=request,

        name="index.html",

        context={}

    )


# ==========================================
# SERVE RESULT IMAGE
# ==========================================

@app.get(
    "/results/{result_type}/{folder_name}/{filename}"
)

async def get_result_image(

    result_type: str,

    folder_name: str,

    filename: str

):

    # --------------------------------------
    # Allow only known result types
    # --------------------------------------

    if result_type not in [

        "detect",

        "obb",

        "segment"

    ]:

        raise HTTPException(

            status_code=400,

            detail="Invalid result type."

        )


    # --------------------------------------
    # Build result path
    # --------------------------------------

    file_path = os.path.join(

        RESULTS_DIR,

        result_type,

        folder_name,

        filename

    )


    print(
        "RESULT IMAGE REQUEST:"
    )

    print(
        file_path
    )


    # --------------------------------------
    # Check if file exists
    # --------------------------------------

    if not os.path.isfile(
        file_path
    ):

        raise HTTPException(

            status_code=404,

            detail="Result image not found."

        )


    # --------------------------------------
    # Return result image
    # --------------------------------------

    return FileResponse(
        file_path
    )


# ==========================================
# ANALYZE IMAGE
# ==========================================

@app.post(
    "/analyze"
)

async def analyze(

    query: str = Form(...),

    image: UploadFile = File(...)

):

    # ======================================
    # SAVE UPLOADED IMAGE
    # ======================================

    file_path = os.path.join(

        UPLOAD_DIR,

        image.filename

    )


    with open(

        file_path,

        "wb"

    ) as buffer:

        shutil.copyfileobj(

            image.file,

            buffer

        )


    # ======================================
    # UNDERSTAND USER QUERY
    # ======================================

    query_result = understand_query(

        query

    )


    # ======================================
    # INITIALIZE RESULTS
    # ======================================

    detection_result = None

    vegetation_result = None

    segmentation_result = None


    # ======================================
    # OBJECT DETECTION
    # ======================================

    if query_result["task"] == "object_detection":


        # ----------------------------------
        # Pass the user's query to the
        # object detector.
        #
        # The detector decides whether
        # to use:
        #
        # YOLO11n
        #
        # OR
        #
        # YOLO26n-OBB
        # ----------------------------------

        detection_result = detect_objects(

            file_path,

            query

        )


        # ----------------------------------
        # Get actual model/result type
        #
        # detect = YOLO11n
        # obb    = YOLO26n-OBB
        # ----------------------------------

        result_type = detection_result[

            "model_type"

        ]


        # ----------------------------------
        # Get output directory
        # ----------------------------------

        output_path = detection_result[

            "output_path"

        ]


        # ----------------------------------
        # Get output folder name
        # ----------------------------------

        folder_name = os.path.basename(

            output_path

        )


        # ----------------------------------
        # Get output filename
        # ----------------------------------

        output_filename = detection_result[

            "output_filename"

        ]


        # ----------------------------------
        # Build correct result image URL
        # ----------------------------------

        detection_result[

            "result_url"

        ] = (

            f"/results/"

            f"{result_type}/"

            f"{folder_name}/"

            f"{output_filename}"

        )


    # ======================================
    # VEGETATION ANALYSIS
    # ======================================

    elif query_result["task"] == "vegetation":


        vegetation_result = (

            analyze_vegetation(

                file_path

            )

        )


    # ======================================
    # IMAGE SEGMENTATION
    # ======================================

    elif query_result["task"] == "segmentation":


        segmentation_result = (

            segment_image(

                file_path

            )

        )


        # ----------------------------------
        # Get output directory
        # ----------------------------------

        output_path = segmentation_result[

            "output_path"

        ]


        # ----------------------------------
        # Get folder name
        # ----------------------------------

        folder_name = os.path.basename(

            output_path

        )


        # ----------------------------------
        # Get output filename
        # ----------------------------------

        output_filename = segmentation_result[

            "output_filename"

        ]


        # ----------------------------------
        # Build segmentation result URL
        # ----------------------------------

        segmentation_result[

            "result_url"

        ] = (

            f"/results/"

            f"segment/"

            f"{folder_name}/"

            f"{output_filename}"

        )


    # ======================================
    # RETURN FINAL RESULT
    # ======================================

    return {

        "status": "success",

        "query": query,

        "image": image.filename,

        "task": query_result[

            "task"

        ],

        "analysis": query_result[

            "analysis"

        ],

        "description": query_result[

            "description"

        ],

        "model_type": query_result[

            "model_type"

        ],

        "detection": detection_result,

        "vegetation": vegetation_result,

        "segmentation": segmentation_result,

        "message": (

            "Query processed successfully."

        )

    }
