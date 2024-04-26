from lib.image_editor import create_cover_image

def main():    
    create_cover_image(
        file_path='./original.jpeg',
        title='LINDAU IN LAKE CONSTANCE',
        subtitle='WALKING TO THE BAVARIAN LION'
    )

if __name__ == "__main__":
    main()
