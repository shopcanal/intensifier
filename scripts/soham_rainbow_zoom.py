import requests
import os
from argparse import ArgumentParser
from tempfile import NamedTemporaryFile

from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def zoom_at(soham_img, x, y, zoom):
    w, h = soham_img.size
    zoom2 = zoom * 2
    soham_img = soham_img.crop((x - w / zoom2, y - h / zoom2, x + w / zoom2, y + h / zoom2))
    return soham_img.resize((w, h), Image.LANCZOS)

parser = ArgumentParser(description='Inputs for the intensifier')
parser.add_argument('-output-path', metavar='op', type=str, help='path to the output')
args = parser.parse_args()

output_path = args.output_path
background_path = os.path.join(BASE_DIR, 'gifs/rainbow_heart.gif')
background_img = Image.open(background_path)

duration = 65

background_imgs = [background_img.copy()]

try:
    while 1:
        background_img.seek(background_img.tell() + 1)
        background_imgs.append(background_img.copy())
except EOFError:
    pass  # end of sequence


soham_url = 'https://emoji.slack-edge.com/T01GP2RMK3R/soham/0d8a223fb974fed9.png'

with NamedTemporaryFile(mode='w+b', delete=True) as temp:
    r = requests.get(soham_url)
    temp.write(r.content)
    soham_img = Image.open(temp.name)
    soham_img = soham_img.convert('RGBA')

background_imgs = [
    img.resize((soham_img.width, soham_img.height), Image.LANCZOS).convert('RGBA')
    for img in background_imgs
]
assert len(background_imgs) == 9


zoom = 1
for i in range(5):
    soham_img = zoom_at(soham_img, int((soham_img.width) / 2), int((soham_img.height) / 2), zoom)
    background_imgs[i].paste(soham_img, (0, 0), mask=soham_img)
    zoom *= 0.9

zoom = 1 / 0.9
for i in range(4):
    soham_img = zoom_at(soham_img, int((soham_img.width) / 2), int((soham_img.height) / 2), zoom)
    background_imgs[i + 5].paste(soham_img, (0, 0), mask=soham_img)
    zoom /= 0.9


background_imgs[0].save(
    fp=output_path,
    format='GIF',
    append_images=background_imgs[1:],
    save_all=True,
    duration=duration,
    loop=0,
    disposal=2,
)
