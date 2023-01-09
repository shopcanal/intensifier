import requests
from string import ascii_lowercase
from tempfile import NamedTemporaryFile

from PIL import Image

from intensifier.utils import intensify_image


alphabet_url = 'https://emoji.slack-edge.com/T01GP2RMK3R/alphabet-yellow-{}/93e76bad666a4f53.png'


for letter in ascii_lowercase:
    with NamedTemporaryFile(mode="w+b", delete=True) as temp:
        r = requests.get(alphabet_url.format(letter))
        temp.write(r.content)
        img = Image.open(temp.name)
    gif_imgs = intensify_image(img)

    gif_imgs[0].save(
        fp=f'/Users/simonxie/Downloads/alphabet_yellows/{letter}-intensifies.gif',
        format="GIF",
        append_images=gif_imgs[1:],
        save_all=True,
        duration=30,
        loop=0,
        disposal=2,
    )
