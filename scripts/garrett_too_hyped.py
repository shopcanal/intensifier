import requests
from argparse import ArgumentParser
from tempfile import NamedTemporaryFile

from PIL import Image, ImageChops


parser = ArgumentParser(description='Inputs for the intensifier')
parser.add_argument('-output-path', metavar='op', type=str, help='path to the output')
args = parser.parse_args()

output_path = args.output_path
assert output_path, 'Output path must be provided'

garrett_hyped_url = 'https://emoji.slack-edge.com/T01GP2RMK3R/garrett-hyped/f79a108375d1271f.png'

with NamedTemporaryFile(mode='w+b', delete=True) as temp:
    r = requests.get(garrett_hyped_url)
    temp.write(r.content)
    img = Image.open(temp.name)


x_offset_inc, y_offset_inc = int(img.width * 0.03), int(img.width * 0.03)
imgs = []

for i in range(4):
    x_offset, y_offset = i * x_offset_inc * -1, i * y_offset_inc
    offset_img = ImageChops.offset(img, x_offset, y_offset)
    offset_img.paste(
        (255, 255, 255, 0),
        (0, 0, img.width, y_offset),
    )
    offset_img.paste(
        (255, 255, 255, 0),
        (0, img.height + y_offset, img.width + x_offset, img.height),
    )
    imgs.append(offset_img)

previous_x_offset, previous_y_offset = x_offset, y_offset_inc

for i in range(4, 7):
    x_offset, y_offset = (previous_x_offset - i * x_offset_inc * -1), (previous_y_offset - i * y_offset_inc)
    offset_img = ImageChops.offset(img, x_offset, y_offset)
    offset_img.paste(
        (255, 255, 255, 0),
        (0, 0, img.width, y_offset),
    )
    offset_img.paste(
        (255, 255, 255, 0),
        (0, img.height + y_offset, img.width + x_offset, img.height),
    )
    imgs.append(offset_img)

imgs[0].save(
    fp=output_path,
    format='GIF',
    append_images=imgs[1:],
    save_all=True,
    duration=60,
    loop=0,
    disposal=2,
)