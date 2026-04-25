import os

path = r"E:\gruha_alankara\app.py"
content = open(path, encoding="utf-8").read()

old_furniture = """        furniture_items = [
            {"name": "Sofa", "quantity": 1, "priority": "HIGH"},
            {"name": "Loveseat", "quantity": 1, "priority": "MEDIUM"},
            {"name": "Armchair", "quantity": 1, "priority": "MEDIUM"},
            {"name": "Coffee Table", "quantity": 1, "priority": "LOW"},
            {"name": "TV Stand", "quantity": 1, "priority": "LOW"},
        ]"""

new_furniture = """        room_furniture_map = {
            "Living Room": [
                {"name": "3-Seater Sofa", "quantity": 1, "priority": "HIGH"},
                {"name": "Coffee Table", "quantity": 1, "priority": "HIGH"},
                {"name": "TV Unit", "quantity": 1, "priority": "MEDIUM"},
                {"name": "Accent Chair", "quantity": 2, "priority": "MEDIUM"},
                {"name": "Floor Lamp", "quantity": 1, "priority": "LOW"},
            ],
            "Bedroom": [
                {"name": "King/Queen Bed", "quantity": 1, "priority": "HIGH"},
                {"name": "Wardrobe", "quantity": 1, "priority": "HIGH"},
                {"name": "Bedside Tables", "quantity": 2, "priority": "MEDIUM"},
                {"name": "Dressing Table", "quantity": 1, "priority": "MEDIUM"},
                {"name": "Study Chair", "quantity": 1, "priority": "LOW"},
            ],
            "Kitchen": [
                {"name": "Kitchen Cabinet", "quantity": 1, "priority": "HIGH"},
                {"name": "Dining Table", "quantity": 1, "priority": "HIGH"},
                {"name": "Dining Chairs", "quantity": 4, "priority": "HIGH"},
                {"name": "Kitchen Island", "quantity": 1, "priority": "MEDIUM"},
                {"name": "Bar Stools", "quantity": 2, "priority": "LOW"},
            ],
            "Bathroom": [
                {"name": "Vanity Cabinet", "quantity": 1, "priority": "HIGH"},
                {"name": "Mirror Cabinet", "quantity": 1, "priority": "HIGH"},
                {"name": "Towel Rack", "quantity": 1, "priority": "MEDIUM"},
                {"name": "Storage Shelf", "quantity": 1, "priority": "MEDIUM"},
                {"name": "Bathroom Stool", "quantity": 1, "priority": "LOW"},
            ],
            "Office": [
                {"name": "Executive Desk", "quantity": 1, "priority": "HIGH"},
                {"name": "Ergonomic Chair", "quantity": 1, "priority": "HIGH"},
                {"name": "Bookshelf", "quantity": 1, "priority": "MEDIUM"},
                {"name": "File Cabinet", "quantity": 1, "priority": "MEDIUM"},
                {"name": "Desk Lamp", "quantity": 1, "priority": "LOW"},
            ],
            "Dining Room": [
                {"name": "Dining Table", "quantity": 1, "priority": "HIGH"},
                {"name": "Dining Chairs", "quantity": 6, "priority": "HIGH"},
                {"name": "Sideboard", "quantity": 1, "priority": "MEDIUM"},
                {"name": "Display Cabinet", "quantity": 1, "priority": "MEDIUM"},
                {"name": "Pendant Light", "quantity": 1, "priority": "LOW"},
            ],
        }
        furniture_items = room_furniture_map.get(room_type, room_furniture_map["Living Room"])"""

if old_furniture in content:
    content = content.replace(old_furniture, new_furniture)
    open(path, "w", encoding="utf-8").write(content)
    print("Furniture fixed by room type!")
else:
    print("Pattern not found - searching...")
    idx = content.find('{"name": "Sofa"')
    if idx > 0:
        print("Found at index:", idx)
        print("Context:", content[idx-50:idx+200])
    else:
        print("Not found in app.py")