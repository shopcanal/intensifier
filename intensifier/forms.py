from typing import Any, Dict

from django import forms


class IntensifierForm(forms.Form):
    image_file = forms.ImageField(required=False)
    image_url = forms.CharField(required=False, help_text="The URL of the image")
    offset_scale = forms.FloatField(
        min_value=0,
        max_value=1,
        required=True,
        initial=0.08,
        help_text="Offset percentage of each frame as a percentage",
    )
    duration = forms.IntegerField(
        min_value=0,
        required=True,
        initial=30,
        help_text="The duration of each frame in 1/100ths of a second",
    )
    remove_background = forms.BooleanField(
        initial=False,
        required=False,
        help_text="Remove the background of the uploaded image",
    )

    def clean(self) -> Dict[str, Any]:
        image_file = self.cleaned_data.get("image_file")
        image_url = self.cleaned_data.get("image_url")
        print(image_url, image_file)
        if not image_file and not image_url:
            raise forms.ValidationError("One of Image Upload or Image URL is required")
        if image_file and image_url:
            raise forms.ValidationError("Only one of Image Upload or Image URL can be chosen")
        return super().clean()
