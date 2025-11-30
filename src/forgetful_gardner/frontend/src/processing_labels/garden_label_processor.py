from enum import StrEnum
from pathlib import Path
from typing import TypedDict, Required, NotRequired, Optional

import cv2
import numpy as np

from .image_processor.image_processor import process_image


class SoilType(StrEnum):
    """Soil Type."""

    draining = "Well drained"
    moist = "Moist"


class PlantPosition(StrEnum):
    """Plant position related to the sun."""

    fullsun = "Full Sun"
    shade = "Partly in Shade"
    indirect = "Indirect Sunlight"


class CareFrequency(StrEnum):
    """Water frequency enum class."""

    weekly = "Weekly"
    fortnightly = "Fortnightly"
    monthly = "Monthly"
    biannual = "Bi-Annually"
    annual = "Yearly"


class PlantCare(TypedDict, total=False):
    """A plant care typed dict."""

    watering_frequency: Required[CareFrequency]
    fertiliser: NotRequired[CareFrequency]
    position: NotRequired[PlantPosition]
    soil: NotRequired[SoilType]


def get_plant_care_text(image_file_path: Path | str) -> Optional[list[str]]:
    """Get the plant care text from a given image.

    Args:
        image: A raw image to be processed.

    Returns:
        A string representing the text from the image.
    """
    image = cv2.imread(str(image_file_path))
    image_text_list = None
    try:
        image_text_list = process_image(image)
    except ValueError:
        print(
            "Could not process the image. Please try to improve the image quality by taking a clearer and close up photo."
        )
    return image_text_list


# I used an LLM to help me turn the get plant care text to one that can process image bytes
def get_plant_care_text_from_image_bytes(image_bytes: bytes) -> Optional[list[str]]:
    """Get the plant care text from a given image.

    Args:
        image: A raw image to be processed.

    Returns:
        A string representing the text from the image.
    """
    np_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Invalid image data")
    image_text_list = None
    try:
        image_text_list = process_image(image)
    except ValueError:
        print(
            "Could not process the image. Please try to improve the image quality by taking a clearer and close up photo."
        )
        raise RuntimeError(
            "Could not process the image. Please try to improve the image quality by taking a clearer and close up photo."
        )
    return image_text_list


# if __name__ == "__main__":

#     test_images = Path("./test/image_processor/test_images/")
#     output_dir = Path("./test/image_processor/test_images/")

#     for image in test_images.iterdir():
#         print("Processing image: ", image)
#         image_text_list = get_plant_care_text(image)
#         if image_text_list is None:
#             print(f"Could not process image: {image}")
#             continue
#         image_text = "\n".join(image_text_list)
#         with (output_dir / "test_images.txt").open(mode="a", encoding="utf-8") as f:
#             f.write(image.stem + "\n" + image_text + "\n")
#             f.write("-----------------------------------------\n")
