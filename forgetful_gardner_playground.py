import marimo

__generated_with = "0.14.7"
app = marimo.App(width="medium")


@app.cell
def _():
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""Pytesseract and OpenCV Playground""")
    return


@app.cell
def _(cv2, get_grayscale, opening, plt, test_images, thresholding):
    image = cv2.imread(str(test_images/"Bacopa.jpg"))
    edited_image =opening(thresholding(get_grayscale(image)))
    plt.imshow(edited_image, "gray")
    return edited_image, image


@app.cell
def _(cv2, get_grayscale, opening, plt, test_images, thresholding):
    image_rotated = cv2.imread(str(test_images/"Dahlia Maggie.jpg"))
    edited_image_rotated =opening(thresholding(get_grayscale(image_rotated)))
    plt.imshow(edited_image_rotated, "gray")
    return (edited_image_rotated,)


@app.cell
def _(RotateFlags, edited_image_rotated, plt, rotate_image):
    rotated_image = rotate_image(edited_image_rotated, RotateFlags.ROTATE_90_CLOCKWISE)
    plt.imshow(rotated_image, "gray")
    return (rotated_image,)


@app.cell
def _():
    config =  fr"--psm 4"
    return (config,)


@app.cell
def _(config, image, image_to_string):
    sample_text = image_to_string(image, config = config)
    return (sample_text,)


@app.cell
def _(sample_text):
    sample_text
    return


@app.cell
def _(config, edited_image, image_to_string):
    edited_sample_text = image_to_string(edited_image, config=config)
    return (edited_sample_text,)


@app.cell
def _(image_to_string, rotated_image):
    image_to_string(rotated_image, config=r"--psm 1")
    return


@app.cell
def _(Output, edited_image_rotated, image_to_string):
    rotated_text = image_to_string(edited_image_rotated, config = r"--psm 1", output_type=Output.STRING)
    rotated_text
    return (rotated_text,)


@app.cell
def _():
    return


@app.cell
def _(Output, edited_image_rotated, image_to_data):
    rotated_data=image_to_data(edited_image_rotated, config=r"--psm 4", output_type=Output.DICT)
    rotated_data
    return (rotated_data,)


@app.cell
def _(rotated_data):
    get_text_quality(rotated_data)
    return


@app.function
def get_text_quality(data):
    lines = {}
    for i in range(len(data['text'])):
        if int(data['conf'][i]) > 60:
            line_num = data['line_num'][i]
            word = data['text'][i]
            if line_num not in lines:
                lines[line_num] = []
            lines[line_num].append(word)
    print(len(lines))
    print(lines)
    for line in lines.values():
        print(' '.join(line))


@app.cell
def _(Output, image_to_data, rotated_image):
    rotated_data_rot = image_to_data(rotated_image, config=r"--psm 4", output_type=Output.DICT)
    rotated_data_rot
    return (rotated_data_rot,)


@app.cell
def _(rotated_data_rot):
    get_text_quality(rotated_data_rot)
    return


@app.cell
def _(rotated_text):
    list(filter(lambda line: line != "" and len(line) > 1,rotated_text.split(".")))
    return


@app.cell
def _(sample_text):
    list(filter(lambda line: line != "" and len(line) > 1,sample_text.split(".")))
    return


@app.cell
def _(edited_sample_text):
    filtered_edited_text = list(filter(lambda line: line != "" and len(line) > 1,edited_sample_text.split(".")))
    filtered_edited_text
    return


@app.cell
def _(Output, config, image, image_to_data):
    sample_data= image_to_data(image=image, config = config, output_type=Output.DICT)
    sample_data["text"]
    return


@app.cell
def _():
    from pathlib import Path
    test_images = Path("./test/image_processor/test_images/")
    return (test_images,)


@app.cell
def _():
    import cv2
    from pytesseract import image_to_data, image_to_string, image_to_osd, Output
    import matplotlib.pyplot as plt
    return Output, cv2, image_to_data, image_to_osd, image_to_string, plt


@app.cell
def _(Output, cv2, image_to_osd, image_to_string):
    import string
    from typing import TypedDict


    class PytesseractOSD(TypedDict, total=True):
        """The PytesseractOSD dictionary output."""

        page_num: int
        orientation: int
        rotate: int
        orientation_conf: float
        script: str
        script_conf: float


    def get_image_text(
        image: cv2.typing.MatLike, config: str = r"-l eng --oem 3 --psm 6"
    ) -> str:
        """Convert image to text.

        Args:
            image: An image to be read.

        Returns:
            A string containing the text from the image.
        """

        custom_config = config + f" -c tessedit_char_whitelist={string.printable}"
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

    return


@app.cell
def _(cv2):
    from enum import IntEnum
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

    return RotateFlags, get_grayscale, opening, rotate_image, thresholding


if __name__ == "__main__":
    app.run()
