from ultralytics import YOLO
import os


# ==========================================
# LOAD SEGMENTATION MODEL
# ==========================================

model = YOLO("yolo11n-seg.pt")


# ==========================================
# SEGMENT IMAGE
# ==========================================

def segment_image(image_path: str):

    # Run segmentation
    results = model(
        image_path,
        save=True,
        conf=0.25
    )

    result = results[0]

    # --------------------------------------
    # Store detected segments
    # --------------------------------------

    segments = []

    if result.masks is not None:

        for index, mask in enumerate(result.masks.data):

            class_id = int(
                result.boxes.cls[index]
            )

            confidence = float(
                result.boxes.conf[index]
            )

            class_name = result.names[
                class_id
            ]

            segments.append({
                "object": class_name,
                "confidence": round(
                    confidence,
                    2
                )
            })

    # --------------------------------------
    # Get YOLO output directory
    # --------------------------------------

    output_dir = str(
        result.save_dir
    )

    # --------------------------------------
    # Find actual output image
    # --------------------------------------

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
            "Segmentation model did not "
            "create an output image."
        )

    # Get output filename
    output_filename = output_files[0]

    # Complete output path
    output_image_path = os.path.join(
        output_dir,
        output_filename
    )

    return {

        "segments": segments,

        "count": len(segments),

        "output_path": output_dir,

        "output_filename": output_filename,

        "output_image_path": output_image_path
    }


# ==========================================
# TESTING
# ==========================================

if __name__ == "__main__":

    test_image = (
        "uploads/satquery1.jpg.jpeg"
    )

    result = segment_image(
        test_image
    )

    print("\nSegmentation Result:")

    print(result)
