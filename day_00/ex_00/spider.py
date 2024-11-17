import requests
from bs4 import BeautifulSoup
import argparse
import os
import sys
from urllib.parse import urljoin, urlparse

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

def recursive_search(url, depth, max_depth, save_path):
    """
        recursively search and download images 
    """

    if depth > max_depth:
        return
    
    try:
        response = session.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all("a", href=True):
                href = link.get('href')
                full_url = urljoin(url, href)

                if is_image_url(full_url):
                    # Download and save the image
                    save_image(full_url, save_path)
                elif href != "../" and depth < max_depth:
                    # Recurse into the link
                    recursive_search(full_url, depth + 1, max_depth, save_path)
        else:
            print(f"Failed to access {url}, status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error with URL {url}: {e}")

def main():
    # Argument parser setup
    parser = argparse.ArgumentParser( description="Spider to download images recursively from a URL.")
    
    parser.add_argument("url", type=str, help="The URL to scrape. This argument is required.",)
    parser.add_argument("-r", action="store_true", help="Enable recursive download.",)
    parser.add_argument("-l", type=int, default=5, help="Set maximum recursive depth level (default: 5).",)
    parser.add_argument("-p", type=str, default="./data/", help="Path to save downloaded files (default: ./data/).",)

    # If no arguments are provided, show an error and usage
    # import sys
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit("Error: Missing required arguments, including the URL to scrape.")

    # Parse arguments
    args = parser.parse_args()

    # Validate save path
    save_path = args.p
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Start the scraping process
    print(f"Starting scraping on {args.url}")
    recursive_search(args.url, depth=0, max_depth=args.l if args.r else 0, save_path=save_path)


if __name__ == "__main__":
    main()