import pandas as pd
import requests
from pathlib import Path
import time
from PIL import Image
from io import BytesIO

def download_images(excel_path):
    # Get the current script's directory to save the images
    image_folder = Path(__file__).parent

    # Load the Excel file, specifying that headers are on the second row (index 1)
    df = pd.read_excel(excel_path, header=0)

    # Total number of rows
    total_images = len(df)
    downloaded_count = 0
    start_time = time.time()

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        url = row['image_url']
        painting_id = row['PaintingId']
        download_start_time = time.time()
        
        # Attempt to download the image
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error on a bad status

            # Check if the response contains a valid image
            try:
                Image.open(BytesIO(response.content)).verify()  # Verify image integrity
            except (IOError, ValueError):
                print(f"Invalid image file received from {url}. Stopping execution.")
                break

            # Write the image to a file using the PaintingId as the filename
            image_path = image_folder / f"{painting_id}.png"
            with open(image_path, 'wb') as file:
                file.write(response.content)

            download_time = time.time() - download_start_time
            downloaded_count += 1
            print(f"Downloaded {url} to {image_path}. Time taken: {download_time:.2f} seconds. Progress: {downloaded_count}/{total_images} images downloaded.")
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            break  # Stop execution on failed download

    total_time = time.time() - start_time
    print(f"All operations complete. Total images downloaded: {downloaded_count}/{total_images}. Total time taken: {total_time:.2f} seconds.")

# Usage
download_images('/Users/jefffan/Desktop/dev/UDP/npm-images-downloader/npm_paintings.xlsx')
