import numpy as np
import pandas as pd
from pathlib import Path

#Paths
TEST_IMAGES_DIR = Path("/kaggle/working/Test_images_1")
OUTPUT_DIR = Path("/kaggle/working/submissions")
OUTPUT_FILE = OUTPUT_DIR / "test_submission.csv"

IMAGE_HEIGHT = 256
IMAGE_WIDTH = 256


def encode_rle(mask):
    """
    Encode a binary mask using Fortran-order RLE.
    """

    pixels = mask.flatten(order="F")

    pixels = np.concatenate([[0], pixels, [0]])

    changes = np.where(pixels[1:] != pixels[:-1])[0] + 1

    changes[1::2] -= changes[::2]

    return " ".join(map(str, changes))


def main():

    OUTPUT_DIR.mkdir(exist_ok=True)

    image_files = sorted([
        path for path in TEST_IMAGES_DIR.iterdir()
        if path.suffix.lower() in {
            ".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"
        }
    ])

    if not image_files:
        raise ValueError("No test images found.")

    predictions = []

    for image_path in image_files:

        #Create an empty binary mask
        mask = np.zeros(
            (IMAGE_HEIGHT, IMAGE_WIDTH),
            dtype=np.uint8
        )

        #Predict a simple rectangular region
        mask[64:192, 96:160] = 1

        #Encode the mask
        encoded_mask = encode_rle(mask)

        predictions.append({
            "image_id": image_path.name,
            "encoded_mask": encoded_mask
        })

    #Save submissionCSV
    df = pd.DataFrame(predictions)

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Submission created: {OUTPUT_FILE}")
    print(f"Number of predictions: {len(df)}")


if __name__ == "__main__":
    main()
