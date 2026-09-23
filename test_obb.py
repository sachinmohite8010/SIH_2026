from ultralytics import YOLO
import os


# ==========================================
# LOAD REMOTE-SENSING OBB MODEL
# ==========================================

model = YOLO("yolo26n-obb.pt")


# ==========================================
# TEST IMAGE
# ==========================================

image_path = "uploads/satquery1.jpg.jpeg"


# ==========================================
# RUN DETECTION
# ==========================================

results = model(
    image_path,
    save=True,
    conf=0.25
)


# ==========================================
# GET RESULT
# ==========================================

result = results[0]


print("\n===================================")
print("REMOTE-SENSING OBB RESULT")
print("===================================")


# ==========================================
# DETECTED OBJECTS
# ==========================================

if result.obb is not None:

    print(
        "\nDetected Objects:",
        len(result.obb)
    )

    for i in range(len(result.obb)):

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
            f"{i + 1}. "
            f"{class_name} "
            f"({confidence * 100:.2f}%)"
        )

else:

    print("\nNo objects detected.")


# ==========================================
# OUTPUT DIRECTORY
# ==========================================

output_dir = str(
    result.save_dir
)

print(
    "\nOutput directory:",
    output_dir
)


# ==========================================
# OUTPUT FILES
# ==========================================

if os.path.exists(output_dir):

    print("\nGenerated files:")

    for file in os.listdir(output_dir):

        print(
            " -",
            file
        )


print(
    "\n==================================="
)
print(
    "OBB TEST COMPLETED"
)
print(
    "==================================="
)
