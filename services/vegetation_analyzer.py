from PIL import Image
import numpy as np


def analyze_vegetation(image_path: str):

    # Open image
    image = Image.open(image_path).convert("RGB")

    # Convert image to NumPy array
    image_array = np.array(image)

    # Separate RGB channels
    red = image_array[:, :, 0].astype(float)
    green = image_array[:, :, 1].astype(float)
    blue = image_array[:, :, 2].astype(float)

    # Simple RGB vegetation index
    vegetation_index = (
        (green - red) /
        (green + red + 1e-6)
    )

    # Pixels considered vegetation
    vegetation_pixels = vegetation_index > 0.15

    # Calculate percentage
    total_pixels = vegetation_index.size

    vegetation_pixel_count = np.sum(
        vegetation_pixels
    )

    vegetation_percentage = (
        vegetation_pixel_count /
        total_pixels
    ) * 100

    # Estimate vegetation level
    if vegetation_percentage >= 60:
        vegetation_level = "High"
    elif vegetation_percentage >= 30:
        vegetation_level = "Moderate"
    else:
        vegetation_level = "Low"

    return {
        "vegetation_percentage": round(
            float(vegetation_percentage),
            2
        ),
        "vegetation_level": vegetation_level,
        "method": "RGB-based vegetation estimation",
        "note": (
            "This is an RGB-based estimate. "
            "True NDVI requires Red and NIR bands."
        )
    }
