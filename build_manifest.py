#!/usr/bin/env python3
"""Rebuild vin-icons.json from the icons/ folder. Run from the repo root."""
import json
import os
import re

USER, REPO, BRANCH = "z285chen", "vin-icons", "main"
ICON_DIR = "icons"                                  # folder name in the repo (used in URLs)
SCAN_DIR = os.environ.get("SCAN_DIR", ICON_DIR)     # where to read files (override for local test)
OUT = os.environ.get("OUT", "vin-icons.json")

# jsDelivr CDN (faster/steadier in China). To use GitHub raw links instead,
# comment the first BASE and uncomment the second.
BASE = f"https://cdn.jsdelivr.net/gh/{USER}/{REPO}@{BRANCH}"
# BASE = f"https://raw.githubusercontent.com/{USER}/{REPO}/{BRANCH}"

EXTS = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg")

# Optional icons/_names.json = {"<filename-without-ext>": "<display name>"} to
# override the auto-derived display names for specific files.
overrides = {}
names_path = os.path.join(SCAN_DIR, "_names.json")
if os.path.exists(names_path):
    with open(names_path, encoding="utf-8") as f:
        overrides = json.load(f)


def display_name(stem):
    if stem in overrides:
        return overrides[stem]
    return re.sub(r"[_\-]+", " ", stem).strip().title()


icons = []
for fn in sorted(os.listdir(SCAN_DIR)):
    if fn.startswith((".", "_")):                   # skip _names.json, dotfiles
        continue
    if not fn.lower().endswith(EXTS):
        continue
    stem = os.path.splitext(fn)[0]
    icons.append({"name": display_name(stem), "url": f"{BASE}/{ICON_DIR}/{fn}"})

data = {"name": "我的图标包", "description": "Vin定制图标需求", "icons": icons}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(f"OK: {OUT} -> {len(icons)} icons")
