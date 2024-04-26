import lib.constants as constants
from PIL import ImageFont
import os
import requests

def download_font(font_name):
    url = constants.FONTS_MAP.get(font_name)
    save_path = os.path.join(constants.FONTS_PATH, f"{font_name}.ttf")
    if not os.path.exists(save_path):
        response = requests.get(url)
        if response.status_code == 200:            
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"Font downloaded and saved to {save_path}")
        else:
            print("Failed to download the font.")
    else:
        print(f"Font already exists at {save_path}")
        
def get_font(font_name='Inter', font_size=30, font_variation=None):
    font_path = os.path.join(constants.FONTS_PATH, f"{font_name}.ttf")
    try:
        font = ImageFont.truetype(font_path, size=font_size)
    except IOError:
        print(f"Font '{font_path}' not found, using default font.")
        font = ImageFont.load_default(size=font_size)
    if font_variation:
        font.set_variation_by_name(font_variation)
        
    return font