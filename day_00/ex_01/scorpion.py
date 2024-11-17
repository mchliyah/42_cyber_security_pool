import requests
# from bs4 import BeautifulSoup
import argparse
import os
import sys
# from urllib.parse import urljoin, urlparse

from PIL import Image, UnidentifiedImageError

session = requests.Session()

# Allowed image extensions
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}


def modify_exif(filename, new_exif_data):
    try:
        img = Image.open(filename)
        exif_data = img._getexif()

        for tag, new_value in new_exif_data.items():
            exif_data[tag] = new_value

        img.save(filename, exif=exif_data)

    except Exception as e:
        print(f"Error modifying EXIF data for {filename}: {e}")


def delete_exif(filename):
    try:
        image = Image.open()

        image.save(filename, exif=None)

    except Exception as e:
        print(f"Error deleting EXIF data for {filename}: {e}")


def print_image_metadata(image_path):
    try:
        # Open the image using Pillow
        img = Image.open(image_path)

        # Define the properties of the image you want to display
        image_properties = {
            'Format': img.format,
            'Size': img.size,
            'Mode': img.mode,
            'Info': img.info  # This will contain extra metadata like EXIF, if available
        }

        # Loop over all the properties and print them
        for key, value in image_properties.items():
            print(f"{key}: {value}")

        # If you want to display EXIF data specifically, you can extract it if available
        if hasattr(img, "_getexif"):
            exif_data = img._getexif()
            if exif_data:
                print("\nEXIF Data:")
                for tag, value in exif_data.items():
                    print(f" {tag}: {value}")

    except Exception as e:
        print(f"Error processing image: {e}")


def main():

    """
        this programe to show the metadata of a given imag with suported type
        as bonus part you may add options as -m or -d to modify or delete the metadata 

    """

    parser = argparse.ArgumentParser( description="scorpion to get metadata from an image")
    
    parser.add_argument("filenames", type=str, nargs="+", help="The file name(s) to process. You can specify one or multiple file names.\nplese provide the file path",)
    parser.add_argument("-m", "--modify", type=str, nargs="+", 
                        help="Modify EXIF data. Provide the tag and value to modify, e.g., -m DateTime '2022:10:20 10:00:00'")
    parser.add_argument("-d", "--delete", action="store_true", 
                        help="Delete EXIF data from the image.")

    # if len(sys.argv) == 1:
    #     parser.print_help()
    #     sys.exit("Error: Missing required arguments, at least a filename must be provided.")

    # Parse arguments
    args = parser.parse_args()

    for filename in args.filenames:
        try:
            # Try opening the image
            print(f"Processing file: {filename}")
            if not os.path.exists(filename):
                print(f"Error: File '{filename}' not found.\nplease check th file path ")
                continue
            else:
                print_image_metadata(filename)

            if args.modify:
                if len(args.modify) % 2 != 0:
                    print("Error: You must provide pairs of tag and value for modification.")
                    continue
                new_exif_data = dict(zip(args.modify[::2], args.modify[1::2]))
                modify_exif(filename, new_exif_data)

            # Delete EXIF if requested and flag is provided
            if args.delete:
                delete_exif(filename)
        except UnidentifiedImageError:
            print(f"Error: File '{filename}' could not be identified as a valid image.")
            continue
        except Exception as e:
            print(f"An unexpected error occurred while processing '{filename}': {e}")
            continue

if __name__ == "__main__":
    main()