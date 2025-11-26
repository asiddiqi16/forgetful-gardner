"""This module describes common image processing utilities.

Reference: https://nanonets.com/blog/ocr-with-tesseract/
"""

from enum import IntEnum

import cv2
import numpy as np


class RotateFlags(IntEnum):
    ROTATE_90_CLOCKWISE = cv2.ROTATE_90_CLOCKWISE
    ROTATE_180 = cv2.ROTATE_180
    ROTATE_90_COUNTERCLOCKWISE = cv2.ROTATE_90_COUNTERCLOCKWISE


def get_grayscale(image: cv2.typing.MatLike) -> cv2.typing.MatLike:
    """Get the grayscale version of the image

    Args:
        image: The image to be processed.

    Returns:
        cv2.typing.MatLike: A grayscale version of the image.
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def remove_noise(image: cv2.typing.MatLike) -> cv2.typing.MatLike:
    """Remove noise from the image.

    Args:
        image: The image to be processed.

    Returns:
        cv2.typing.MatLike: An image with noise reduced.
    """
    return cv2.medianBlur(image, 5)


def thresholding(image: cv2.typing.MatLike) -> cv2.typing.MatLike:
    """Apply a threshold to the image to get a black-white image.

    Generally applied after applying grayscale.

    Args:
        image: The image to be processed.

    Returns:
        cv2.typing.MatLike: An image with an applied threshold to get black and white image.
    """
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


def dilate(image: cv2.typing.MatLike) -> cv2.typing.MatLike:
    """Dilate the image.

    Args:
        image: The image to be processed.

    Returns:
        cv2.typing.MatLike: A dilated image."""
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


def erode(image: cv2.typing.MatLike) -> cv2.typing.MatLike:
    """Erode the image.

    Args:
        image: The image to be processed.

    Returns:
        cv2.typing.MatLike: An eroded image."""
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image: cv2.typing.MatLike) -> cv2.typing.MatLike:
    """Erode the image then dilate.

    Args:
        image: The image to be processed.

    Returns:
        cv2.typing.MatLike: An eroded and dilated image."""
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# canny edge detection
def canny(image: cv2.typing.MatLike) -> cv2.typing.MatLike:
    """Detect edges in the image.

    Args:
        image: The image to be processed.

    Returns:
        cv2.typing.MatLike: An image with edges detected."""
    return cv2.Canny(image, 100, 200)


def rotate_image(
    image: cv2.typing.MatLike, rotation_angle: RotateFlags
) -> cv2.typing.MatLike:
    """Rotate the image by the given angle.

    Args:
        image: The image to be processed.

    Returns:
        cv2.typing.MatLike: A rotated image."""
    return cv2.rotate(image, rotation_angle)


# skew correction
def deskew(image: cv2.typing.MatLike) -> cv2.typing.MatLike:
    """Deskew the images.

    Args:
        image: The image to be processed.

    Returns:
        cv2.typing.MatLike: An image that has been deskewed."""
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    m = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        image,
        m,
        (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE,
    )
    return rotated


# template matching
def match_template(image: cv2.typing.MatLike, template: cv2.typing.MatLike):
    """Applies a template to the image.

    Args:
        image: The image to be processed.

    Returns:
        cv2.typing.MatLike: An image that has been matched to a template."""
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
