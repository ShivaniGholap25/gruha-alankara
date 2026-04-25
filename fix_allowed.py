import re

content = open("E:/gruha_alankara/app.py", encoding="utf-8").read()

old = '''def allowed_file(filename):
    allowed_extensions = {"png", "jpg", "jpeg"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions'''

new = '''def allowed_file(filename):
    allowed_extensions = {"png", "jpg", "jpeg", "webp", "gif", "bmp"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions'''

if old in content:
    content = content.replace(old, new)
    print("Found and replaced!")
else:
    print("Pattern not found, searching...")
    idx = content.find("def allowed_file")
    print("Function at index:", idx)
    print("Current function:")
    print(content[idx:idx+200])

open("E:/gruha_alankara/app.py", "w", encoding="utf-8").write(content)
