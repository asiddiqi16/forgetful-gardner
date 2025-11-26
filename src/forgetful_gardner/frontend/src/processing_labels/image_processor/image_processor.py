from typing import Optional

import cv2
from pytesseract.pytesseract import TesseractError


from .image_utils import (
    get_grayscale,
    thresholding,
    opening,
    rotate_image,
    RotateFlags,
)
from .image_reader import (
    get_image_text,
    get_image_orientation,
    get_image_data,
    get_text_read_quality,
    analyse_image_quality_text,
)


def process_image(image: cv2.typing.MatLike) -> list[str]:
    """Process the image to prepare for reading.

    Args:
        image: An image to be processed.

    Returns:
        A string representing the text from the image.

    Raises:
        ValueError: If the image cannot be processed or read.
    """
    denoise = opening(image)
    grayed = get_grayscale(denoise)
    thresh = thresholding(grayed)
    image_text: str = ""
    cv2_rotation: Optional[RotateFlags] = determine_image_rotation(thresh)
    if cv2_rotation is not None:
        image_to_read = rotate_image(thresh, cv2_rotation)
    else:
        image_to_read = thresh
    # Attempt default config read and check quality.
    try:
        image_text = analyse_image_quality_text(image_to_read)
    except ValueError:
        # If the default config read fails, try a more lenient config.
        try:
            image_text = analyse_image_quality_text(image_to_read, config=r"--psm 1")
        except ValueError:
            raise

    text_list: list = list(
        filter(lambda line: line != "" and len(line) > 1, image_text.split("."))
    )
    return text_list


def determine_image_rotation(image: cv2.typing.MatLike) -> Optional[RotateFlags]:
    """Determine the rotation of the image.
    Args:
        image: An image to be processed.
    Returns:
        A RotateFlags enum value representing the rotation of the image.
    """

    try:
        image_orientation = get_image_orientation(image)
        cv2_rotation: Optional[RotateFlags]
        match image_orientation["rotate"]:
            case 90:
                cv2_rotation = RotateFlags.ROTATE_90_CLOCKWISE
            case 180:
                cv2_rotation = RotateFlags.ROTATE_180
            case 270:
                cv2_rotation = RotateFlags.ROTATE_90_COUNTERCLOCKWISE
            case _:
                cv2_rotation = None
    except TesseractError:
        # Couldn't process the image. Ignore rotation
        cv2_rotation = None
    return cv2_rotation
