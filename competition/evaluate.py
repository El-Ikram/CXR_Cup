# competition/evaluate.py

import pandas as pd
import numpy as np
import sys

from pathlib import Path
from PIL import Image

from metrics import (
    dice_score,
    decode_rle,
    IMAGE_HEIGHT,
    IMAGE_WIDTH
)

from validate_submission import main as validate_submission


MASK_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"
}


def find_ground_truth_mask(mask_dir, image_id):

    image_stem = Path(image_id).stem

    matches = [
        path for path in mask_dir.iterdir()
        if path.is_file()
        and path.stem == image_stem
        and path.suffix.lower() in MASK_EXTENSIONS
    ]

    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one ground-truth mask for {image_id}, "
            f"found {len(matches)}."
        )

    return matches[0]


def main(pred_path, test_images_dir, test_masks_dir):

    # Validate submission first
    validate_submission(pred_path, test_images_dir)

    preds = pd.read_csv(pred_path)

    test_masks_dir = Path(test_masks_dir)

    if not test_masks_dir.exists():
        raise FileNotFoundError(
            f"Test masks directory not found: {test_masks_dir}"
        )

    scores = []

    for _, row in preds.iterrows():

        image_id = row["image_id"]

        # Decode predicted mask
        predicted_mask = decode_rle(
            row["encoded_mask"],
            IMAGE_HEIGHT,
            IMAGE_WIDTH
        )

        # Find corresponding ground-truth mask
        mask_path = find_ground_truth_mask(
            test_masks_dir,
            image_id
        )

        # Load ground-truth mask
        with Image.open(mask_path) as image:
            ground_truth = np.array(image.convert("L"))

        if ground_truth.shape != (IMAGE_HEIGHT, IMAGE_WIDTH):
            raise ValueError(
                f"Ground-truth mask {mask_path.name} "
                f"has an unexpected size: {ground_truth.shape}"
            )

        # Convert ground-truth mask to binary
        ground_truth = (ground_truth > 0).astype(np.uint8)

        # Calculate Dice Score
        score = dice_score(ground_truth, predicted_mask)

        scores.append(score)

    # Macro-average across images
    final_score = float(np.mean(scores))

    print(f"SCORE={final_score:.8f}")


if __name__ == "__main__":

    if len(sys.argv) != 4:
        raise ValueError(
            "Usage: python evaluate.py "
            "<predictions.csv> <test_images_directory> "
            "<test_masks_directory>"
        )

    main(sys.argv[1], sys.argv[2], sys.argv[3])
