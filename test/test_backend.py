from pathlib import Path
import time
import requests

from forgetful_gardner.processing_labels.garden_label_processor import (
    get_plant_care_text,
)

BACKEND_URL = "http://localhost:8001/extract"

questions = [
    """Jasminum azoricum

ter of white

be fom late spring to
autumn
 This jasmine has dark green glossy
foliage that contrasts well with the white
flowers

Position: Full sun to part shade

Soll: Prefers any well drained garden soiL

Watering: Moderate water requirement

A twinning clim

Fertilise: Use a long-term controlled-release
fertiliser in spring and autumn


Use: It can form an attractive rambling shrub
or be trained on a trellis, fence or archway,
for support, where it mild Perfume will fill the
summer nights

Growing Tips: Will toler

; ate light fros
in a warm position in ful g ts but does

sun or part shade


Spring to Late
Autumn""",
    """Acer Palmaturn ‘Osakazukj
JAPANESE MAPLE
A small, deciduous

» OfNamenta| tree 9rown for
elegant form and decorative foliage


Maples for
@ Moist, fertile Soils With
SUN or S€Mi-shade
 Frost

ree when Young
 Mulch to
O! Weeds
 Do NOt allow #5""",
]

# request_bodies = [{"ocr_text": q} for q in questions]

# start_time = time.perf_counter()
# try:
#     outputs = [requests.post(BACKEND_URL, json=data) for data in request_bodies]
# except Exception as e:
#     print(e)
# end_time = time.perf_counter()

# print(f"Run time: {end_time - start_time} seconds")
# print([output.json() for output in outputs])

test_images = Path("./test/image_processor/test_images/")
output_dir = Path("./test/image_processor/test_images/")

for image in test_images.glob("*.jpg"):
    print("Processing image: ", image)
    image_text_list = get_plant_care_text(image)
    if image_text_list is None:
        print(f"Could not process image: {image}")
        continue
    else:
        image_text = "\n".join(image_text_list)
        care_data = requests.post(BACKEND_URL, json={"ocr_text": image_text})
        print(f"Care responsE: {care_data.text}")

    with (output_dir / "test_images_caredata.text").open(
        mode="a", encoding="utf-8"
    ) as f:
        f.write(image_text)
        f.write("___________________________")
        f.write(care_data.text)
