# competition/metrics.py

import numpy as np

IMAGE_HEIGHT = 256
IMAGE_WIDTH = 256


def decode_rle(encoded_mask, height=IMAGE_HEIGHT, width=IMAGE_WIDTH):
    """
    Decode a Run-Length Encoded mask.

    Convention:
    - Fortran (column-major) order
    - 1-based indexing
    - Space-separated start-length pairs
    """

    if not isinstance(encoded_mask, str):
        raise ValueError("RLE mask must be a string.")

    encoded_mask = encoded_mask.strip()

    if not encoded_mask:
        return np.zeros((height, width), dtype=np.uint8)

    values = encoded_mask.split()

    if len(values) % 2 != 0:
        raise ValueError("Invalid RLE: expected start-length pairs.")

    try:
        values = [int(value) for value in values]
    except ValueError:
        raise ValueError("RLE must contain integers only.")

    starts = values[0::2]
    lengths = values[1::2]

    total_pixels = height * width
    flat_mask = np.zeros(total_pixels, dtype=np.uint8)

    for start, length in zip(starts, lengths):

        if start < 1 or length < 1:
            raise ValueError("RLE positions and lengths must be positive.")

        start_index = start - 1
        end_index = start_index + length

        if end_index > total_pixels:
            raise ValueError("RLE mask exceeds the expected image dimensions.")

        flat_mask[start_index:end_index] = 1

    return flat_mask.reshape((height, width), order="F")


def dice_score(y_true, y_pred):
    """
    Calculate the Dice Similarity Coefficient.

    Returns a value between 0 and 1.
    """

    y_true = np.asarray(y_true).astype(bool)
    y_pred = np.asarray(y_pred).astype(bool)

    if y_true.shape != y_pred.shape:
        raise ValueError("Ground-truth and predicted masks must have the same shape.")

    intersection = np.logical_and(y_true, y_pred).sum()

    denominator = y_true.sum() + y_pred.sum()

    if denominator == 0:
        return 1.0

    return float(2.0 * intersection / denominator)
