import random


def get_fallback_design(style_theme):
    style_data = {
        "Modern Minimalist": {
            "furniture": ["Low-profile sofa", "Glass coffee table", "Geometric shelving", "Platform bed", "Accent chair"],
            "colors": ["#FFFFFF", "#000000", "#808080", "#F5F5F5"],
            "materials": ["Glass", "Steel", "Concrete", "Light wood"],
        },
        "Scandinavian": {
            "furniture": ["Platform Bed", "Dresser", "Nightstand", "Wooden Desk", "Accent Chair"],
            "colors": ["#F5F0E8", "#2C5F2E", "#D4A373", "#FEFAE0"],
            "materials": ["Pine wood", "Linen", "Wool", "Ceramic"],
        },
        "Industrial": {
            "furniture": ["Leather Sofa", "Metal Bookshelf", "Concrete Coffee Table", "Iron Floor Lamp", "TV Stand"],
            "colors": ["#2E2E2E", "#5A5A5A", "#8C7B75", "#B0A8A0"],
            "materials": ["Raw steel", "Exposed brick", "Concrete", "Distressed wood"],
        },
        "Bohemian": {
            "furniture": ["Rattan Chair", "Patterned Ottoman", "Low Coffee Table", "Hanging Lamp", "Open Shelf"],
            "colors": ["#E76F51", "#2A9D8F", "#E9C46A", "#F4A261"],
            "materials": ["Rattan", "Jute", "Cotton weave", "Carved wood"],
        },
        "Traditional": {
            "furniture": ["Tufted Sofa", "Carved Side Table", "Classic Armchair", "Wood Console", "Display Cabinet"],
            "colors": ["#7A4E2D", "#C9B79C", "#8B0000", "#F5E6CC"],
            "materials": ["Teak wood", "Brass", "Velvet", "Marble"],
        },
        "Contemporary": {
            "furniture": ["Modular Sofa", "Accent Chair", "Smart TV Unit", "Glass Center Table", "Statement Lamp"],
            "colors": ["#D9D9D9", "#4A4E69", "#9A8C98", "#F2E9E4"],
            "materials": ["Tempered glass", "Matte metal", "Engineered wood", "Textured fabric"],
        },
    }
    data = style_data.get(style_theme, style_data["Modern Minimalist"])
    return {
        "furniture": data["furniture"],
        "color_scheme": data["colors"],
        "materials": data["materials"],
        "placement_tips": f"Arrange furniture to maximize space flow for {style_theme} style.",
    }


def generate_design(image_path, style_theme):
    return get_fallback_design(style_theme)
