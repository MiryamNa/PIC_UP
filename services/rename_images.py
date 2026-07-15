import os
import re
from pathlib import Path


def clean_filename(filename: str) -> str:
    name, ext = os.path.splitext(filename)

    # הסרת תווים בלתי נראים
    name = "".join(c for c in name if c.isprintable())

    # החלפת רווחים ב־_
    name = name.replace(" ", "_")

    # השארת אותיות אנגליות, מספרים, _, -
    name = re.sub(r"[^A-Za-z0-9_-]", "", name)

    # מניעת שמות ריקים
    if not name:
        name = "image"

    return name + ext.lower()

# folder = Path(FOLDER)
#
# for file in folder.iterdir():
#     if not file.is_file():
#         continue
#
#     if file.suffix.lower() not in [".jpg", ".jpeg", ".png", ".bmp", ".gif"]:
#         continue
#
#     new_name = clean_filename(file.name)
#
#     if file.name == new_name:
#         continue
#
#     target = file.parent / new_name
#
#     counter = 1
#     while target.exists():
#         stem = Path(new_name).stem
#         suffix = Path(new_name).suffix
#         target = file.parent / f"{stem}_{counter}{suffix}"
#         counter += 1
#
#     print(f"{file.name}  -->  {target.name}")
#
#     file.rename(target)
#
# print("Done")