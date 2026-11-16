#!/usr/bin/env python3
"""Rebuild vin-icons.json and the QX-compatible icons from the icons/ folder.

Run from the repo root. Source icons in icons/ are never modified; each one is
scaled into icons/qx/ as a 144x144 RGBA PNG for Quantumult X.
"""
import json
import os

from PIL import Image

USER, REPO, BRANCH = "z285chen", "vin-icons", "main"
ICON_DIR = "icons"                                  # folder name in the repo (used in URLs)
SCAN_DIR = os.environ.get("SCAN_DIR", ICON_DIR)     # where to read files (override for local test)
QX_DIR = os.path.join(ICON_DIR, "qx")               # QX-compatible copies (144x144 RGBA)
QX_SIZE = (144, 144)
OUT = os.environ.get("OUT", "vin-icons.json")

# GitHub raw: QX fetches the images directly, so keep the plain raw URLs.
BASE = f"https://raw.githubusercontent.com/{USER}/{REPO}/{BRANCH}"

EXTS = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg")

# Optional icons/_names.json = {"<filename-without-ext>": "<name>"} to override
# the filename QX sees for specific files. A .png suffix is always appended.
overrides = {}
names_path = os.path.join(SCAN_DIR, "_names.json")
if os.path.exists(names_path):
    with open(names_path, encoding="utf-8") as f:
        overrides = json.load(f)


def icon_name(stem):
    name = overrides.get(stem, stem)
    return name if name.lower().endswith(".png") else f"{name}.png"


os.makedirs(QX_DIR, exist_ok=True)

icons = []
for fn in sorted(os.listdir(SCAN_DIR)):
    if fn.startswith((".", "_")):                   # skip _names.json, dotfiles
        continue
    if not fn.lower().endswith(EXTS):
        continue
    stem = os.path.splitext(fn)[0]
    with Image.open(os.path.join(SCAN_DIR, fn)) as img:
        img.convert("RGBA").resize(QX_SIZE, Image.LANCZOS).save(
            os.path.join(QX_DIR, f"{stem}.png"), format="PNG"
        )
    icons.append(
        {"name": icon_name(stem), "url": f"{BASE}/{QX_DIR}/{stem}.png"}
    )

data = {"name": "我的图标包", "description": "Vin定制图标需求", "icons": icons}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(f"OK: {OUT} -> {len(icons)} icons")
