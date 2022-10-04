import sys
from PIL import Image

input_path = sys.argv[1]
im = Image.open(input_path)

try:
    duration = sys.argv[2]
except Exception:
    duration = 30

imgs = [im.copy()]

try:
    while 1:
        im.seek(im.tell() + 1)
        imgs.append(im.copy())
except EOFError:
    pass  # end of sequence

# imgs[0].save(
#     fp=input_path,
#     format='GIF',
#     append_images=imgs[1:],
#     save_all=True,
#     duration=duration,
#     loop=0,
#     disposal=2,
# )
