import requests
from argparse import ArgumentParser
from tempfile import NamedTemporaryFile

from PIL import Image, ImageChops, ImageOps

parser = ArgumentParser(description="Inputs for the intensifier")
parser.add_argument("-output-path", metavar="op", type=str, help="path to the output")
args = parser.parse_args()

output_path = args.output_path
assert output_path, "Output path must be provided"

toby_proud_url = (
    "https://emoji.slack-edge.com/T01GP2RMK3R/toby-liftoff/c940a71a6d277b95.gif"
)

with NamedTemporaryFile(mode="w+b", delete=True) as temp:
    r = requests.get(toby_proud_url)
    temp.write(r.content)
    img = Image.open(temp.name)

img = img.convert("RGBA")

x_offset_inc, y_offset_inc = int(img.width / 8), int(img.width / 8)

ul_imgs = []
ul_img = img.copy()
for i in range(8):
    x_offset, y_offset = i * x_offset_inc * -1, i * y_offset_inc * -1
    offset_img = ImageChops.offset(ul_img, x_offset, y_offset)
    offset_img.paste(
        (255, 255, 255, 0),
        (img.width + x_offset, 0, img.width, img.height + y_offset),
    )
    offset_img.paste(
        (255, 255, 255, 0),
        (0, img.height + y_offset, img.width + x_offset, img.height),
    )
    ul_imgs.append(offset_img)

ur_imgs = []
ur_img = ImageOps.mirror(img)
for i in range(8):
    x_offset, y_offset = i * x_offset_inc, i * y_offset_inc * -1
    offset_img = ImageChops.offset(ur_img, x_offset, y_offset)
    offset_img.paste(
        (255, 255, 255, 0),
        (0, 0, x_offset, img.height + y_offset),
    )
    offset_img.paste(
        (255, 255, 255, 0),
        (x_offset, img.height + y_offset, img.width, img.height),
    )
    ur_imgs.append(offset_img)


dr_imgs = []
dr_img = ImageOps.mirror(ImageOps.flip(img))
for i in range(8):
    x_offset, y_offset = i * x_offset_inc, i * y_offset_inc
    offset_img = ImageChops.offset(dr_img, x_offset, y_offset)
    offset_img.paste(
        (255, 255, 255, 0),
        (0, y_offset, x_offset, img.height),
    )
    offset_img.paste(
        (255, 255, 255, 0),
        (x_offset, 0, img.width, y_offset),
    )
    dr_imgs.append(offset_img)

dl_imgs = []
dl_img = ImageOps.flip(img)
for i in range(8):
    x_offset, y_offset = i * x_offset_inc * -1, i * y_offset_inc
    offset_img = ImageChops.offset(dl_img, x_offset, y_offset)
    offset_img.paste(
        (255, 255, 255, 0),
        (img.width + x_offset, y_offset, img.width, img.height),
    )
    offset_img.paste(
        (255, 255, 255, 0),
        (0, 0, img.width + x_offset, y_offset),
    )
    dl_imgs.append(offset_img)

output_imgs = []
for ul_img, ur_img, dr_img, dl_img in zip(ul_imgs, ur_imgs, dr_imgs, dl_imgs):
    output_img = Image.new("RGBA", (img.width * 2, img.height * 2))
    output_img.paste(ul_img, (0, 0))
    output_img.paste(ur_img, (img.width, 0))
    output_img.paste(dr_img, (img.width, img.height))
    output_img.paste(dl_img, (0, img.height))
    output_imgs.append(output_img)

output_imgs[0].save(
    fp=output_path,
    format="GIF",
    append_images=output_imgs[1:],
    save_all=True,
    duration=60,
    loop=0,
    disposal=2,
)
