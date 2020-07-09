from django import forms
from .models import Image
from django.utils.text import slugify
from urllib import request
from django.core.files.base import ContentFile

class ImageCreationForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("title" , "description" , 'url')
        widgets = {
            'url' : forms.HiddenInput
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        if url is None:
            raise forms.ValidationError("The url field is required to bookmark an image")
        valid_extensions = ['jpg', 'jpeg']
        url_extension = url.rsplit(".", 1)[1].lower()
        if url_extension not in valid_extensions:
            raise forms.ValidationError("The given URL does not match the valid image extensions")
        return url

    def save(self, commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit(".", 1)[1].lower()
        image_name = "{}.{}".format(name, extension)

        # Download image from the given url
        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()), save=False)

        if commit:
            image.save()
        return image

