from ultralytics import YOLO
import os


# ============================================================
# LOAD MODELS
# ============================================================

# Generic object detection model
generic_model = YOLO("yolo11n.pt")


# Remote-sensing / aerial OBB model
remote_sensing_model = YOLO("yolo26n-obb.pt")


# ============================================================
# DOTA / REMOTE-SENSING OBJECT KEYWORDS
# ============================================================

REMOTE_SENSING_KEYWORDS = [

    "plane",
    "planes",

    "aircraft",

    "ship",
    "ships",

    "vehicle",
    "vehicles",

    "helicopter",
    "helicopters",

    "storage tank",
    "storage tanks",

    "baseball diamond",

    "basketball court",

    "soccer ball field",

    "tennis court",

    "ground track field",

    "harbor",
    "harbour",

    "bridge",

    "roundabout",

    "swimming pool"
]


# ============================================================
# DETERMINE WHICH MODEL TO USE
# ============================================================

def should_use_remote_sensing_model(query: str):

    query = query.lower().strip()

    for keyword in REMOTE_SENSING_KEYWORDS:

        if keyword in query:

            return True

    return False


# ============================================================
# OBJECT DETECTION
# ============================================================

def detect_objects(
    image_path: str,
    query: str = ""
):

    # ========================================================
    # SELECT MODEL
    # ========================================================

    use_remote_sensing = (
        should_use_remote_sensing_model(query)
    )


    if use_remote_sensing:

        model = remote_sensing_model

        model_used = (
            "YOLO26n-OBB "
            "(DOTA Remote-Sensing Model)"
        )

        result_type = "obb"

    else:

        model = generic_model

        model_used = (
            "YOLO11n "
            "(Generic Object Detection Model)"
        )

        result_type = "detect"


    print("\n======================================")
    print("SATQUERY OBJECT DETECTION")
    print("======================================")

    print(
        "Query:",
        query
    )

    print(
        "Model:",
        model_used
    )


    # ========================================================
    # RUN MODEL
    # ========================================================

    results = model(
        image_path,
        save=True,
        conf=0.25
    )

    result = results[0]


    # ========================================================
    # STORE DETECTED OBJECTS
    # ========================================================

    detected_objects = []


    # ========================================================
    # REMOTE-SENSING OBB RESULT
    # ========================================================

    if use_remote_sensing:

        if result.obb is not None:

            for i in range(
                len(result.obb)
            ):

                class_id = int(
                    result.obb.cls[i]
                )

                confidence = float(
                    result.obb.conf[i]
                )

                class_name = result.names[
                    class_id
                ]


                # --------------------------------------------
                # OBB COORDINATES
                # --------------------------------------------

                coordinates = (
                    result.obb.xyxyxyxy[i]
                    .cpu()
                    .numpy()
                    .tolist()
                )


                detected_objects.append({

                    "object": class_name,

                    "confidence": round(
                        confidence,
                        2
                    ),

                    "type": "oriented_bounding_box",

                    "coordinates": coordinates
                })


    # ========================================================
    # GENERIC YOLO RESULT
    # ========================================================

    else:

        if result.boxes is not None:

            for box in result.boxes:

                class_id = int(
                    box.cls[0]
                )

                confidence = float(
                    box.conf[0]
                )

                class_name = result.names[
                    class_id
                ]


                detected_objects.append({

                    "object": class_name,

                    "confidence": round(
                        confidence,
                        2
                    ),

                    "type": "bounding_box"
                })


    # ========================================================
    # GET OUTPUT DIRECTORY
    # ========================================================

    output_dir = str(
        result.save_dir
    )


    # ========================================================
    # FIND ACTUAL OUTPUT IMAGE
    # ========================================================

    output_files = [

        file

        for file in os.listdir(
            output_dir
        )

        if os.path.isfile(
            os.path.join(
                output_dir,
                file
            )
        )

    ]


    if not output_files:

        raise FileNotFoundError(
            "Object detection model "
            "did not create an output image."
        )


    # ========================================================
    # OUTPUT IMAGE
    # ========================================================

    output_filename = (
        output_files[0]
    )


    output_image_path = os.path.join(

        output_dir,

        output_filename
    )


    # ========================================================
    # FINAL RESULT
    # ========================================================

    return {

        "detected_objects":
            detected_objects,

        "count":
            len(detected_objects),

        "model_used":
            model_used,

        "model_type":
            result_type,

        "output_path":
            output_dir,

        "output_filename":
            output_filename,

        "output_image_path":
            output_image_path
    }


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    test_image = (
        "uploads/satquery1.jpg.jpeg"
    )


    test_query = (
        "Detect aircraft in this satellite image"
    )


    result = detect_objects(

        test_image,

        test_query
    )


    print(
        "\nDetection Result:"
    )

    print(
        result
    )
