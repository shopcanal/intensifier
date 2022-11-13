from random import shuffle
from typing import List

from PIL import Image, ImageChops
from rembg import remove


def intensify_image(
    img: Image.Image,
    offset_scale: float = 0.08,
    remove_bg: bool = False,
) -> List[Image.Image]:
    img = img.convert("RGBA")
    if remove_bg:
        img = remove(img)
    x_offset, y_offset = int(img.width * offset_scale), int(img.height * offset_scale)
    rd_img = offset_image(img, x_offset, y_offset)
    u_img = offset_image(img, 0, y_offset * -1)
    lu_img = offset_image(img, x_offset * -1, y_offset * -1)
    d_img = offset_image(img, 0, y_offset * -1)
    ru_img = offset_image(img, x_offset, y_offset * -1)
    r_img = offset_image(img, x_offset, 0)
    ld_img = offset_image(img, x_offset * -1, y_offset)
    l_img = offset_image(img, x_offset * -1, 0)
    gif_imgs = [img, rd_img, u_img, lu_img, d_img, ru_img, r_img, ld_img, l_img]
    shuffle(gif_imgs)
    return gif_imgs


def offset_image(img: Image.Image, x_offset: int, y_offset: int) -> Image.Image:
    img = img.convert("RGBA")
    offset_img = ImageChops.offset(img, x_offset, y_offset)
    if x_offset > 0:
        offset_img.paste((255, 255, 255, 0), (0, 0, x_offset, img.height))
    elif x_offset < 0:
        offset_img.paste(
            (255, 255, 255, 0), (img.width + x_offset, 0, img.width, img.height)
        )

    if y_offset > 0:
        offset_img.paste((255, 255, 255, 0), (0, 0, img.width, y_offset))
    elif y_offset < 0:
        offset_img.paste(
            (255, 255, 255, 0), (0, img.height + y_offset, img.width, img.height)
        )

    return offset_img
