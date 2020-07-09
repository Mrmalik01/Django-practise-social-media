from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreationForm

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
            return redirect(image.get_absolute_url())
        else:
            image_form = ImageCreationForm(data=request.GET)
    return render(request, "images/image/create.html", {
        "section" : "images",
        "form" : image_form
    })

