# CRX_Cup

# Chest X-ray Lung Segmentation Challenge

## About the Competition

Welcome to the Chest X-ray Lung Segmentation Challenge!

The objective is to develop an image segmentation model that identifies and segments the lung regions in chest X-ray images.

## Task

Participants must predict a binary segmentation mask for every provided test image.

- Lung pixels: 1
- Background pixels: 0

## Dataset

The dataset is sourced from Kaggle:

[Chest X-ray Lungs Segmentation](https://www.kaggle.com/datasets/iamtapendu/chest-x-ray-lungs-segmentation)

## Task Type

Binary Semantic Segmentation.

## Baseline

A U-Net implementation is provided as a starting point.

## Evaluation

Submissions will be evaluated using the Dice Score.

## Rules

1. Use the provided training dataset.
2. Do not access or attempt to reconstruct hidden test masks.
3. Follow the required mask submission format.
4. External datasets and pretrained models must be disclosed.
5. Respect the dataset's original license and terms.

## Repository Structure

- `src/`: Dataset preparation, models and evaluation.
- `notebooks/`: Experiments and visualizations.
- `configs/`: Training configurations.
- `docs/`: Competition documentation.

## Contact

For questions, use the GitHub Issues section.
