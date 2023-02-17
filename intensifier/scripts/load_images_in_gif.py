import sys
from PIL import Image

from rembg import remove

input_path = sys.argv[1]
try:
    remove_background = bool(sys.argv[2])
except Exception:
    remove_background = False
im = Image.open(input_path)

imgs = [im.copy()]

try:
    while 1:
        im.seek(im.tell() + 1)
        imgs.append(im.copy())
except EOFError:
    pass  # end of sequence
if remove_background:
    new_imgs = []
    for img in imgs:
        new_imgs.append(remove(img))
    imgs = new_imgs

imgs[0].save(
    fp=input_path,
    format="GIF",
    append_images=imgs[1:],
    save_all=True,
    duration=im.info["duration"],
    loop=0,
    disposal=2,
)
