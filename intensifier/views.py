import requests
from tempfile import NamedTemporaryFile

from django.http import FileResponse, HttpRequest
from django.shortcuts import render
from PIL import Image

from intensifier.forms import IntensifierForm
from intensifier.utils import intensify_image


def intensify_image_view(request: HttpRequest):
    if request.method == "POST":
        intensifier_form = IntensifierForm(request.POST, request.FILES)
        if intensifier_form.is_valid():
            cleaned_data = intensifier_form.cleaned_data
            image_file = cleaned_data["image_file"]
            image_url = cleaned_data["image_url"]
            duration = cleaned_data["duration"]
            remove_background = cleaned_data["remove_background"]
            offset_scale = cleaned_data["offset_scale"]
            if image_file:
                img = Image.open(image_file.file, mode="r")
            else:
                with NamedTemporaryFile(mode="w+b", delete=True) as temp:
                    r = requests.get(image_url)
                    temp.write(r.content)
                    img = Image.open(temp.name)
            gif_imgs = intensify_image(
                img=img, offset_scale=offset_scale, remove_bg=remove_background
            )
            with NamedTemporaryFile(mode="w+b", delete=True) as temp:
                gif_imgs[0].save(
                    fp=temp.name,
                    format="GIF",
                    append_images=gif_imgs[1:],
                    save_all=True,
                    duration=duration,
                    loop=0,
                    disposal=2,
                )

                return FileResponse(
                    open(temp.name, "rb"),
                    as_attachment=True,
                    filename="intensifies.gif",
                )
        else:
            render(request, "index.html", {"intensifier_form": intensifier_form})
    else:
        intensifier_form = IntensifierForm()

    return render(request, "index.html", {"intensifier_form": intensifier_form})
