from lib.image_editor import create_cover_image

def main():    
    create_cover_image(
        file_path='./original.png',
        title='No Title',
        subtitle='No Subtitle',
        transparency=0.65,
        title_font_size=90,
        subtitle_font_size=60
    )

if __name__ == "__main__":
    main()
