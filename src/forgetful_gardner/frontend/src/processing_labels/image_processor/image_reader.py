from typing import TypedDict

import cv2
from pytesseract import image_to_string, image_to_osd, image_to_data, Output


class PytesseractOSD(TypedDict, total=True):
    """The PytesseractOSD dictionary output."""

    page_num: int
    orientation: int
    rotate: int
    orientation_conf: float
    script: str
    script_conf: float


def get_image_data(image: cv2.typing.MatLike, config: str = r"--psm 4") -> dict:
    """Get the image data in Output.DICT format

    Args:
        image: An image to be read.

    Returns:
        A dictionary containing the text data from the image.
    """
    custom_config = config
    text_data = image_to_data(image, config=custom_config, output_type=Output.DICT)
    return text_data


def get_image_text(image: cv2.typing.MatLike, config: str = r"--psm 4") -> str:
    """Convert image to text.

    Args:
        image: An image to be read.

    Returns:
        A string containing the text from the image.
    """
    custom_config = config
    text = image_to_string(image, config=custom_config)
    return text


def get_image_orientation(image: cv2.typing.MatLike) -> PytesseractOSD:
    """Get the image orientation.

    Args:
        image: An image to be read.

    Returns:
        A string containing the image and script orientation.
    """
    return image_to_osd(image, output_type=Output.DICT)


def get_text_read_quality(
    image_data: dict, confidence: int = 60, line_threshold: int = 2
) -> bool:
    """Get the text read quality.

    Args:
        image_data (dict): A dictionary containing the pytesseract image OutputDICT data.
        line_threshold (int): The number of lines to determine good quality.

    Returns:
        A boolean to indicate whether the text is good or poor quality.
            True is good quality.
            False is poor quality.
    """
    lines: dict = {}
    for i in range(len(image_data["text"])):
        if int(image_data["conf"][i]) > confidence:
            line_num = image_data["line_num"][i]
            word = image_data["text"][i]
            if line_num not in lines:
                lines[line_num] = []
            lines[line_num].append(word)
    if len(lines) > line_threshold:
        return True
    return False


def analyse_image_quality_text(image: cv2.typing.MatLike, config=r"--psm 4") -> str:
    """Get the text from the image.

    Args:
        image: An image to be processed.

    Returns:
        A string containing the text from the image.

    Raises:
        ValueError: If the image text read quality is too low.
    """
    image_data = get_image_data(image, config=config)
    if get_text_read_quality(image_data):
        image_text = get_image_text(image, config=config)
        return image_text
    else:
        raise ValueError(
            "Image text read quality is too low. Please check the image quality."
        )
