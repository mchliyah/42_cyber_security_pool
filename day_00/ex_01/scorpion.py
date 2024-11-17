import requests
import bs4 as bs
import argparse
import os
import sys
from urllib.parse import urljoin, urlparse

from PIL import Image, UnidentifiedImageError

session = requests.Session()

# Allowed image extensions
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}


def is_image_url(url):
    """
    Check if a URL points to an image file based on its extension.
    """
    return any(url.lower().endswith(ext) for ext in IMAGE_EXTENSIONS)


def save_image(url, save_path):
    """
    Download and save an image from a URL.
    """
    try:
        response = session.get(url, stream=True)
        if response.status_code == 200:
            # Extract file name from URL
            file_name = os.path.basename(urlparse(url).path)
            file_path = os.path.join(save_path, file_name)

            # Save the image
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Saved: {file_path}")
        else:
            print(f"Failed to download {url}, status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

# def recursive_search(url, depth, max_depth, save_path):
#     """
#         recursively from PIL import Image
#     if depth > max_depth:
#         return
    
#     try:
#         responsfrom PIL import Image full_url = urljoin(url, href)

#                 if is_image_url(full_url):
#                     # Download and save the image
#                     save_image(full_url, save_path)
#                 elif href != "../" and depth < max_depth:
#                     # Recurse into the link
#                     recursive_search(full_url, depth + 1, max_depth, save_path)
#         else:from PIL import Image
#             print(f"Failed to access {url}, status code: {response.status_code}")
#     except requests.exceptions.RequestException as e:
#         print(f"Error with URL {url}: {e}")

def main():
    # Argument parser setup
    parser = argparse.ArgumentParser( description="scorpion to get metadata from an image")
    
    parser.add_argument("filenames", type=str, nargs="+", help="The file name(s) to process. You can specify one or multiple file names.\
                                                                 plese provide the file path",)
    # If no arguments are provided, show an error and usage
    # import sys
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit("Error: Missing required arguments, at least a filename must be provided.")

    # Parse arguments
    args = parser.parse_args()

    for filename in args.filenames:
        try:
            # Try opening the image
            print(f"Processing file: {filename}")
            with Image.open(filename) as img:
                print(f"Successfully opened {filename}")
                # You can add more metadata processing here if needed
                print(f"Image format: {img.format}, Size: {img.size}, Mode: {img.mode}")
        
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.\nplease check th file path ")
        except UnidentifiedImageError:
            print(f"Error: File '{filename}' could not be identified as a valid image.")
        except Exception as e:
            print(f"An unexpected error occurred while processing '{filename}': {e}")


    # recursive_search(args.url, depth=0, max_depth=args.l if args.r else 0, save_path=save_path)


if __name__ == "__main__":
    main()