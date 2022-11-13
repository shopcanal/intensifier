import os
import requests
import sys
from argparse import ArgumentParser
from tempfile import NamedTemporaryFile

import validators
from PIL import Image

from intensifier.utils import intensify_image

parser = ArgumentParser(description="Inputs for the intensifier")

parser.add_argument("-u", metavar="u", type=str, help="url of the image")
parser.add_argument("-p", metavar="p", type=str, help="path to local image")
parser.add_argument("-o", metavar="o", type=str, help="path to the output")
parser.add_argument(
    "-offset-scale", metavar="os", type=float, help="offset scale of the intensity"
)
parser.add_argument("-duration", metavar="d", type=int, help="duration of the gif")
parser.add_argument("-remove-bg", metavar="r", type=bool, help="removes the background")
parser.add_argument("-only-png", metavar="op", type=bool, help="Only save the png")

args = parser.parse_args()
url, path, output_path, offset_scale, duration = (
    args.u,
    args.p,
    args.o,
    args.offset_scale or 0.08,
    args.duration or 30,
)
assert url or path, "URL or path must be provided"
assert output_path, "Output path must be provided"
assert 0 < offset_scale < 1 and duration > 0
if url:
    if not validators.url(url):
        raise Exception(f"{url} is an invalid url")
    print("URL input")
    with NamedTemporaryFile(mode="w+b", delete=True) as temp:
        r = requests.get(url)
        temp.write(r.content)
        img = Image.open(temp.name)

else:
    assert os.path.isfile(path), f"{path} is an invalid filepath"
    print("Filepath input")
    img = Image.open(path)

if args.only_png:
    img.save(output_path)
    sys.exit()

x_offset, y_offset = int(img.width * offset_scale), int(img.height * offset_scale)

gif_imgs = intensify_image(img, offset_scale, args.remove_bg)
gif_imgs[0].save(
    fp=output_path,
    format="GIF",
    append_images=gif_imgs[1:],
    save_all=True,
    duration=duration,
    loop=0,
    disposal=2,
)
