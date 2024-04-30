from PIL import Image, ImageDraw, ImageFont
import os
import lib.constants as constants
from lib.fonts import download_font
from lib.fonts import get_font

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
    transparency = int(255 * 0.75)
    fill_color = (0, 0, 0, transparency)
    fill_color_red = (90, 0, 0, transparency)
    fill_color = fill_color_red
    # Create a drawing context with transparency support
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    overlay = Image.new('RGBA', image.size)
    draw = ImageDraw.Draw(overlay)  # Create a draw object for the overlay

    # Draw the semi-transparent black box
    draw.rectangle(black_box_position, fill=fill_color)

    # Load and set title font
    title_font = get_font(font_name, title_font_size, font_variation="Bold")
    subtitle_font = get_font(font_name, subtitle_font_size)    
    
    vertical_shift = -60
    
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

    # Determine the scale to apply based on the main image dimensions while maintaining aspect ratio
    original_width, original_height = overlay_image.size
    aspect_ratio = original_width / original_height

    # Calculate new dimensions based on aspect ratio
    new_height = int(image.height * scale_factor)
    new_width = int(new_height * aspect_ratio)

    # Resize the overlay image using LANCZOS resampling, maintaining aspect ratio
    overlay_image = overlay_image.resize((new_width, new_height), Image.LANCZOS)

    # Position the overlay in the top left corner (adjust as necessary)
    position = (40, 40)  # Adjust this if needed

    # Paste the overlay image onto the main image at the specified position, ensuring alpha is used if present
    image.paste(overlay_image, position, overlay_image if overlay_image.mode == 'RGBA' else None)
    
def create_cover_image(
    file_path='./original.jpeg', 
    output_path='./out/output.jpg',
    title='Example Title',
    subtitle='Example Subtitle',
):
    main_image = Image.open(file_path).convert('RGBA')  # Ensure it's in RGBA mode

    main_image = create_title_overlay(
        main_image, 
        title=title,
        subtitle=subtitle,
        font_name='Inter'
    )

    # Apply image overlay, scaled to 10%
    add_image_overlay(main_image, './assets/images/4k.png', 0.1)

    # Save the final image
    main_image = main_image.convert('RGB')

    # Try different quality values if necessary to fit the file size requirement
    quality = 85
    main_image.save(output_path, 'JPEG', quality=quality)

    # Check the file size and reduce quality if necessary
    if os.path.getsize(output_path) > 2 * 1024 * 1024:
        print("Adjusting quality to reduce file size...")
        # Decrease the quality in steps and save again if needed
        while quality > 10 and os.path.getsize(output_path) > 2 * 1024 * 1024:
            quality -= 5
            main_image.save(output_path, 'JPEG', quality=quality)

    print(f"Final image saved with quality {quality}")