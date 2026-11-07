# competition/validate_submission.py

import pandas as pd
import sys

from pathlib import Path

from metrics import decode_rle, IMAGE_HEIGHT, IMAGE_WIDTH


REQUIRED_COLUMNS = {"image_id", "encoded_mask"}

IMAGE_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"
}


def main(pred_path, test_images_dir):

    preds = pd.read_csv(pred_path)

    test_images_dir = Path(test_images_dir)

    if not test_images_dir.exists():
        raise FileNotFoundError(
            f"Test images directory not found: {test_images_dir}"
        )

    # Check required columns
    if not REQUIRED_COLUMNS.issubset(preds.columns):
        raise ValueError(
            "Submission must contain columns: image_id, encoded_mask"
        )

    # Check empty values
    if preds["image_id"].isna().any():
        raise ValueError("Missing image IDs found.")

    if preds["encoded_mask"].isna().any():
        raise ValueError("Missing encoded masks found.")

    preds["image_id"] = preds["image_id"].astype(str)

    # Check duplicate IDs
    if preds["image_id"].duplicated().any():
        raise ValueError("Duplicate image IDs found.")

    # Get expected test image IDs (including file extensions)
    test_image_ids = {
        path.name
        for path in test_images_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    }

    submitted_ids = set(preds["image_id"])

    # Check exact ID match
    if submitted_ids != test_image_ids:
        missing = test_image_ids - submitted_ids
        extra = submitted_ids - test_image_ids

        raise ValueError(
            f"Image ID mismatch. Missing: {len(missing)}, "
            f"Extra: {len(extra)}"
        )

    # Validate every RLE mask
    for _, row in preds.iterrows():

        try:
            decode_rle(
                row["encoded_mask"],
                IMAGE_HEIGHT,
                IMAGE_WIDTH
            )

        except ValueError as error:
            raise ValueError(
                f"Invalid RLE for image {row['image_id']}: {error}"
            )

    print("VALID_SUBMISSION")


if __name__ == "__main__":

    if len(sys.argv) != 3:
        raise ValueError(
            "Usage: python validate_submission.py "
            "<predictions.csv> <test_images_directory>"
        )

    main(sys.argv[1], sys.argv[2])
