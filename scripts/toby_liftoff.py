import requests
from argparse import ArgumentParser
from tempfile import NamedTemporaryFile

from PIL import Image, ImageChops

parser = ArgumentParser(description='Inputs for the intensifier')
parser.add_argument('-output-path', metavar='op', type=str, help='path to the output')
args = parser.parse_args()

output_path = args.output_path
assert output_path, 'Output path must be provided'

toby_proud_url = 'https://emoji.slack-edge.com/T01GP2RMK3R/toby-proud/c309da6571270472.png'

with NamedTemporaryFile(mode='w+b', delete=True) as temp:
    r = requests.get(toby_proud_url)
    temp.write(r.content)
    img = Image.open(temp.name)

x_offset_inc, y_offset_inc = int(img.width / 8), int(img.width / 8)
imgs = []

for i in range(8):
    x_offset, y_offset = i * x_offset_inc * -1, i * y_offset_inc * -1
    offset_img = ImageChops.offset(img, x_offset, y_offset)
    offset_img.paste(
        (255, 255, 255, 0),
        (img.width + x_offset, 0, img.width, img.height + y_offset),
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
