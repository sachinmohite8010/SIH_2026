from ultralytics import YOLO
import os


# ==========================================
# LOAD OBB MODEL
# ==========================================

model = YOLO("yolo26n-obb.pt")


# ==========================================
# DOTA VALIDATION IMAGES
# ==========================================

image_dir = "dota8/images/val"


# ==========================================
# OUTPUT DIRECTORY
# ==========================================

output_dir = "runs/dota_obb_test"

os.makedirs(
    output_dir,
    exist_ok=True
)


# ==========================================
# FIND IMAGES
# ==========================================

images = [
    os.path.join(image_dir, file)
    for file in os.listdir(image_dir)
    if file.lower().endswith(
        (".jpg", ".jpeg", ".png")
    )
]


print("\n======================================")
print("DOTA REMOTE-SENSING OBB TEST")
print("======================================")


print(
    "\nImages found:",
    len(images)
)


# ==========================================
# PROCESS EACH IMAGE
# ==========================================

total_objects = 0


for image_path in images:

    print("\n--------------------------------------")

    print(
        "Image:",
        os.path.basename(image_path)
    )

    results = model(
        image_path,
        conf=0.25,
        save=True,
        project=output_dir,
        name="results",
        exist_ok=True
    )

    result = results[0]


    # ======================================
    # CHECK DETECTIONS
    # ======================================

    if result.obb is not None:

        count = len(result.obb)

    else:

        count = 0


    total_objects += count


    print(
        "Objects detected:",
        count
    )


    # ======================================
    # PRINT OBJECT CLASSES
    # ======================================

    if count > 0:

        for i in range(count):

            class_id = int(
                result.obb.cls[i]
            )

            confidence = float(
                result.obb.conf[i]
            )

            class_name = result.names[
                class_id
            ]

            print(
                f"  {i + 1}. "
                f"{class_name} "
                f"({confidence * 100:.1f}%)"
            )

    else:

        print(
            "  No objects detected."
        )


# ==========================================
# FINAL SUMMARY
# ==========================================

print("\n======================================")
print("FINAL SUMMARY")
print("======================================")

print(
    "Images tested:",
    len(images)
)

print(
    "Total objects detected:",
    total_objects
)

print(
    "\nResults saved inside:"
)

print(
    os.path.abspath(output_dir)
)

print(
    "\n======================================"
)
print(
    "DOTA OBB TEST COMPLETED"
)
print(
    "======================================"
)
