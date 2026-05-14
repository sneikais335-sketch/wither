import os
from PIL import Image

def prepare_icons():
    # Attempt to load the provided image and convert to app icon
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    source_img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "photo_5429185189155376072_y.jpg")
    
    if os.path.exists(source_img_path):
        try:
            img = Image.open(source_img_path)
            img = img.resize((256, 256), Image.LANCZOS)
            
            icon_ico = os.path.join(assets_dir, "icon.ico")
            icon_png = os.path.join(assets_dir, "icon.png")
            
            img.save(icon_ico, format="ICO", sizes=[(256,256),(128,128),(64,64),(32,32),(16,16)])
            img.save(icon_png)
            print("Icons generated successfully.")
        except Exception as e:
            print(f"Error generating icons: {e}")
    else:
        print("Source image not found for icon generation. Assuming default CTk icon.")

# Can be called during setup/first run
