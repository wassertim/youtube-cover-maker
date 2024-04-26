import lib.constants as constants
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