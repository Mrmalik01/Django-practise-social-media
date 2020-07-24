from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreationForm
from .models import Image

# Create your views here.
@login_required
def image_create(request):
    if request.method == "POST":
        image_form = ImageCreationForm(data=request.POST)
        if image_form.is_valid():
            image = image_form.save(commit=False)
            image.user = request.user
            image.save()
            messages.success(request, "Image added successfully")
            print(image.get_absolute_url)
            return redirect(image.get_absolute_url())
    else:
        image_form = ImageCreationForm(data=request.GET)

    return render(request, "images/image/create.html", {
        "section" : "images",
        "form" : image_form
    })

def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request,
                  'images/image/detail.html',
                  {"section" : "images",
                   "image" : image})
