import os
import shutil
import sys

import cv2
from PIL import Image
from rembg import remove

os.makedirs("output", exist_ok=True)
input_path = sys.argv[1]
output_path = sys.argv[2]

cap = cv2.VideoCapture(input_path)
still_reading, image = cap.read()
frame_count = 0
frame_skip = 3
imgs = []
while still_reading:

    image_output_path = f"output/frame_{frame_count:03d}.png"
    cv2.imwrite(image_output_path, image)
    pil_img = Image.open(image_output_path)
    removed_bg = remove(pil_img)
    removed_bg.save(image_output_path)
    removed_bg = removed_bg.resize(
        (int(removed_bg.width / 8), int(removed_bg.height / 8))
    )
    imgs.append(removed_bg)
    for _ in range(frame_skip):
        still_reading, image = cap.read()
    frame_count += 1

imgs[0].save(
    fp=output_path,
    format="GIF",
    append_images=imgs[1:],
    save_all=True,
    duration=20,
    loop=0,
    disposal=2,
)

shutil.rmtree("output")
