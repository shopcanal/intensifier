import os
import requests
from argparse import ArgumentParser
from tempfile import NamedTemporaryFile

import validators
from PIL import Image, ImageChops

parser = ArgumentParser(description='Inputs for the intensifier')

parser.add_argument('-u', metavar='u', type=str, help='url of the image')
parser.add_argument('-p', metavar='p', type=str, help='path to local image')
parser.add_argument('-output-path', metavar='op', type=str, help='path to the output')
parser.add_argument('-offset-scale', metavar='os', type=float, help='offset scale of the intensity')
parser.add_argument('-duration', metavar='d', type=int, help='duration of the gif')

args = parser.parse_args()
url, path, output_path, offset_scale, duration = args.u, args.p, args.output_path, args.offset_scale or 0.08, args.duration or 30
assert url or path, 'URL or path must be provided'
assert output_path, 'Output path must be provided'
assert 0 < offset_scale < 1 and duration > 0
if url:
    if not validators.url(url):
        raise Exception(f'{url} is an invalid url')
    print("URL input")
    with NamedTemporaryFile(mode='w+b', delete=True) as temp:
        r = requests.get(url)
        temp.write(r.content)
        img = Image.open(temp.name)

else:
    assert os.path.isfile(path), f'{path} is an invalid filepath'
    print("Filepath input")
    img = Image.open(path)
    base_path, _ = os.path.splitext(path)

img = img.convert('RGBA')

x_offset, y_offset = int(img.width * offset_scale), int(img.height * offset_scale)

# right down offset
rd_img = ImageChops.offset(img, x_offset, y_offset)
rd_img.paste((255, 255, 255, 0), (0, 0, x_offset, img.height))
rd_img.paste((255, 255, 255, 0), (0, 0, img.width, y_offset))

# up offset
u_img = ImageChops.offset(img, 0, y_offset * -1)
u_img.paste((255, 255, 255, 0), (0, img.height - y_offset, img.width, img.height))

# left up offset
lu_img = ImageChops.offset(img, x_offset * -1, y_offset * -1)
lu_img.paste((255, 255, 255, 0), (img.width - x_offset, 0, img.width, img.height))
lu_img.paste((255, 255, 255, 0), (0, img.height - y_offset, img.width, img.height))

# down offset
d_img = ImageChops.offset(img, 0, y_offset * -1)
d_img.paste((255, 255, 255, 0), (0, img.height - y_offset, img.width, img.height))

# right up
ru_img = ImageChops.offset(img, x_offset, y_offset * -1)
ru_img.paste((255, 255, 255, 0), (0, 0, x_offset, img.height))
ru_img.paste((255, 255, 255, 0), (0, img.height - y_offset, img.width, img.height))

# right
r_img = ImageChops.offset(img, x_offset, 0)
r_img.paste((255, 255, 255, 0), (0, 0, x_offset, img.height))

# left down
ld_img = ImageChops.offset(img, x_offset * -1, y_offset)
ld_img.paste((255, 255, 255, 0), (img.width - x_offset, 0, img.width, img.height))
ld_img.paste((255, 255, 255, 0), (0, 0, img.width, y_offset))

# left
l_img = ImageChops.offset(img, x_offset * -1, 0)
l_img.paste((255, 255, 255, 0), (img.width - x_offset, 0, img.width, img.height))


gif_imgs = (rd_img, u_img, lu_img, d_img, ru_img, r_img, ld_img, l_img)
gif = img
img.save(
    fp=output_path,
    format='GIF',
    append_images=gif_imgs,
    save_all=True,
    duration=duration,
    loop=0,
    disposal=2,
)
