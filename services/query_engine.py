def understand_query(query: str):
    """
    Understand the user's natural-language query
    and identify the required remote-sensing analysis.
    """

    query = query.lower().strip()

    # -----------------------------------------
    # Keywords
    # -----------------------------------------

    vegetation_keywords = [
        "vegetation",
        "forest",
        "crop",
        "crops",
        "plant",
        "plants",
        "greenery",
        "ndvi",
        "vegetation health"
    ]

    land_cover_keywords = [
        "land cover",
        "landcover",
        "classify land",
        "classification",
        "water bodies",
        "urban area",
        "built-up",
        "built up"
    ]

    object_detection_keywords = [
        "detect",
        "detection",
        "find buildings",
        "buildings",
        "vehicles",
        "roads",
        "aircraft",
        "ships"
    ]

    segmentation_keywords = [
        "segment",
        "segmentation",
        "outline",
        "mask",
        "pixel level",
        "pixel-level"
    ]

    change_detection_keywords = [
        "change",
        "changes",
        "changed",
        "before and after",
        "compare images",
        "difference between",
        "construction progress"
    ]

    # -----------------------------------------
    # Change Detection
    # -----------------------------------------

    if any(keyword in query for keyword in change_detection_keywords):

        return {
            "task": "change_detection",
            "analysis": "Change Detection",
            "description": "Compare images to identify changes over time.",
            "model_type": "Change Detection Model",
            "matched_keywords": [
                keyword
                for keyword in change_detection_keywords
                if keyword in query
            ]
        }

    # -----------------------------------------
    # Segmentation
    # -----------------------------------------

    if any(keyword in query for keyword in segmentation_keywords):

        return {
            "task": "segmentation",
            "analysis": "Image Segmentation",
            "description": "Divide the satellite image into meaningful regions.",
            "model_type": "Segmentation Model",
            "matched_keywords": [
                keyword
                for keyword in segmentation_keywords
                if keyword in query
            ]
        }

    # -----------------------------------------
    # Object Detection
    # -----------------------------------------

    if any(keyword in query for keyword in object_detection_keywords):

        return {
            "task": "object_detection",
            "analysis": "Object Detection",
            "description": "Detect and locate objects in the satellite image.",
            "model_type": "Object Detection Model",
            "matched_keywords": [
                keyword
                for keyword in object_detection_keywords
                if keyword in query
            ]
        }

    # -----------------------------------------
    # Land Cover
    # -----------------------------------------

    if any(keyword in query for keyword in land_cover_keywords):

        return {
            "task": "land_cover",
            "analysis": "Land Cover Classification",
            "description": "Identify different land-cover categories.",
            "model_type": "Land Cover Classification Model",
            "matched_keywords": [
                keyword
                for keyword in land_cover_keywords
                if keyword in query
            ]
        }

    # -----------------------------------------
    # Vegetation
    # -----------------------------------------

    if any(keyword in query for keyword in vegetation_keywords):

        return {
            "task": "vegetation",
            "analysis": "Vegetation Analysis",
            "description": "Analyze vegetation or vegetation-related information.",
            "model_type": "Remote Sensing Vegetation Model",
            "matched_keywords": [
                keyword
                for keyword in vegetation_keywords
                if keyword in query
            ]
        }

    # -----------------------------------------
    # Unknown Query
    # -----------------------------------------

    return {
        "task": "unknown",
        "analysis": "Unknown Analysis",
        "description": "The query could not be mapped to a supported analysis.",
        "model_type": None,
        "matched_keywords": []
    }


# -----------------------------------------
# Testing
# -----------------------------------------

if __name__ == "__main__":

    test_queries = [
        "Detect buildings in this satellite image",
        "Analyze vegetation in this image",
        "Classify the land cover",
        "Segment the buildings",
        "Compare these images and find changes"
    ]

    for query in test_queries:

        result = understand_query(query)

        print("\nQuery:", query)
        print("Result:", result)
