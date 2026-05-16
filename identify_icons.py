from PIL import Image
import os
import math

files = [f for f in os.listdir("/home/sneikais/Desktop/Untitled") if f.startswith("SVG") or f.startswith("Vector")]
for f in sorted(files):
    p = os.path.join("/home/sneikais/Desktop/Untitled", f)
    if os.path.isfile(p):
        try:
            with Image.open(p) as img:
                print(f"{f}: {img.size}, mode={img.mode}")
        except Exception as e:
            print(f"{f}: Error {e}")
