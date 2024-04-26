from PIL import Image, ImageDraw, ImageFont
import os
import lib.constants as constants
from lib.fonts import download_font
        
def create_title_overlay(image, title, subtitle, font_name="Inter", title_font_size=110, subtitle_font_size=65):
    download_font(font_name)
    font_path = os.path.join(constants.FONTS_PATH, f"{font_name}.ttf")
    # Calculate the position and size based on the image dimensions
    width = image.width
    height = int(image.height * 0.35)
    x = 0
    y = image.height - height

    # Define the position and size of the black box with transparency
    black_box_position = (x, y, x + width, y + height)
    transparency = int(255 * 0.75)  # 55% transparency
    fill_color = (0, 0, 0, transparency)  # RGBA where A is alpha for transparency
    fill_color_red = (90, 0, 0, transparency)  # RGBA where A is alpha for transparency
    fill_color = fill_color_red
    # Create a drawing context with transparency support
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    overlay = Image.new('RGBA', image.size)
    draw = ImageDraw.Draw(overlay)  # Create a draw object for the overlay

    # Draw the semi-transparent black box
    draw.rectangle(black_box_position, fill=fill_color)

    # Load and set title font
    try:
        title_font = ImageFont.truetype(font_path, size=title_font_size)
    except IOError:
        print(f"Title font '{font_path}' not found, using default font.")
        title_font = ImageFont.load_default(size=title_font_size)
    title_font.set_variation_by_name("Bold")
    # Load and set subtitle font
    try:
        subtitle_font = ImageFont.truetype(font_path, size=subtitle_font_size)
    except IOError:
        print(f"Subtitle font '{font_path}' not found, using default font.")
        subtitle_font = ImageFont.load_default(size=subtitle_font_size)
    vertical_shift = -60
    # Calculate title text position
    title_text_bbox = draw.textbbox((x, y), title, font=title_font)
    title_text_width = title_text_bbox[2] - title_text_bbox[0]
    title_text_height = title_text_bbox[3] - title_text_bbox[1]
    title_text_position = (x + (width - title_text_width) // 2, y + (height // 2 - title_text_height) + vertical_shift)
    
    gap = 0

    # Calculate subtitle text position
    subtitle_text_bbox = draw.textbbox((x, y), subtitle, font=subtitle_font)
    subtitle_text_width = subtitle_text_bbox[2] - subtitle_text_bbox[0]
    subtitle_text_height = subtitle_text_bbox[3] - subtitle_text_bbox[1]
    subtitle_text_position = (x + (width - subtitle_text_width) // 2, y + (height // 2 + subtitle_text_height // 2) + gap)

    color_white_with_alpha = (255, 255, 255, 200)
    # Draw the title and subtitle in white
    draw.text(title_text_position, title, font=title_font, fill=color_white_with_alpha)

    draw.text(subtitle_text_position, subtitle, font=subtitle_font, fill=color_white_with_alpha)

    # Composite the overlay onto the original image
    image = Image.alpha_composite(image, overlay)

    return image

def add_image_overlay(image, overlay_image_path, scale_factor):
    # Load the overlay image
    overlay_image = Image.open(overlay_image_path)

    # Calculate the new size as 10% of the original image size
    new_width = int(image.width * scale_factor)
    new_height = int(image.height * scale_factor)
    
    # Resize the overlay image using LANCZOS resampling
    overlay_image = overlay_image.resize((new_width, new_height), Image.LANCZOS)

    # Position the overlay in the top left corner
    position = (40, 40)  # Top left corner of the main image

    # Paste the overlay image onto the main image at the specified position
    image.paste(overlay_image, position, overlay_image)


# Usage example
def main():    
    # Load the main image
    main_image = Image.open('./original.jpeg').convert('RGBA')  # Ensure it's in RGBA mode

    # Apply text overlay
    main_image = create_title_overlay(
        main_image, 
        title='LINDAU IN LAKE CONSTANCE',
        subtitle='WALKING TO THE BAVARIAN LION',
        font_name='Inter'
    )

    # Apply image overlay, scaled to 10%
    add_image_overlay(main_image, './assets/images/4k.png', 0.1)

    # Save the final image
    main_image = main_image.convert('RGB')

    # Try different quality values if necessary to fit the file size requirement
    quality = 85
    main_image.save('./out/output.jpg', 'JPEG', quality=quality)

    # Check the file size and reduce quality if necessary
    if os.path.getsize('./out/output.jpg') > 2 * 1024 * 1024:
        print("Adjusting quality to reduce file size...")
        # Decrease the quality in steps and save again if needed
        while quality > 10 and os.path.getsize('./out/output.jpg') > 2 * 1024 * 1024:
            quality -= 5
            main_image.save('./out/output.jpg', 'JPEG', quality=quality)

    print(f"Final image saved with quality {quality}")

    # Display the image for verification (optional)
    main_image.show()

if __name__ == "__main__":
    main()
