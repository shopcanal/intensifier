import requests
from tempfile import NamedTemporaryFile

from PIL import Image

from intensifier.utils import offset_image

url = 'https://emoji.slack-edge.com/T01GP2RMK3R/garrett/22e2802a41806a45.png'

with NamedTemporaryFile(mode="w+b", delete=True) as temp:
    r = requests.get(url)
    temp.write(r.content)
    img = Image.open(temp.name)

imgs = []


zoom = 0.1
for i in range(18):
    offset_img = Image.new('RGBA', img.size)
    zoomed_img = img.resize((int(img.width * zoom), int(img.height * zoom)))
    offset_img.paste(zoomed_img, (0, img.height - zoomed_img.height))
    offset_img = Image.new('RGBA', img.size)
    
    zoomed_img = img.resize((int(img.width * zoom), int(img.height * zoom)))
    offset_img.paste(zoomed_img, (0, img.height - zoomed_img.height))
    first_img = offset_image(offset_img, 0, -2)
    second_img = offset_image(offset_img, 2, 0)
    third_img = offset_image(offset_img, 2, -2)
    imgs.extend([first_img, second_img, third_img])
    zoom += 0.05
imgs.extend([third_img] * 8)

imgs[0].save(
    fp='/Users/simonxie/Downloads/garrett-arrive.gif',
    format="GIF",
    append_images=imgs[1:],
    save_all=True,
    duration=70,
    loop=0,
    disposal=2,
)
