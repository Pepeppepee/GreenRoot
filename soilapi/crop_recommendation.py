CROP_RECOMMENDATIONS = {
    "Alluvial soil": ["Cauliflower", "Cabbage", "Spinach"],
    "Clay soil": ["Cauliflower", "Spinach"],
    "Black soil": ["Potato", "Tomato"],
    "Red soil": ["Potato", "Spinach"]
}

def recommend_crops(soil_type):
    return CROP_RECOMMENDATIONS.get(soil_type, [])
