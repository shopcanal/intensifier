import asyncio
import requests
from argparse import ArgumentParser
from tempfile import NamedTemporaryFile

from deeppyer import deepfry

from PIL import Image, ImageChops

parser = ArgumentParser(description="Inputs for the intensifier")
parser.add_argument("-u", metavar="u", type=str, help="url of the image")
parser.add_argument("-output-path", metavar="op", type=str, help="path to the output")
args = parser.parse_args()

url, output_path = args.u, args.output_path
assert url and output_path, "URL and Output path must be provided"

with NamedTemporaryFile(mode="w+b", delete=True) as temp:
    r = requests.get(url)
    temp.write(r.content)
    img = Image.open(temp.name)
    img = img.convert("RGBA")

loop = asyncio.get_event_loop()
deep_fried = loop.run_until_complete(deepfry(img))
deep_fried.save(output_path)
