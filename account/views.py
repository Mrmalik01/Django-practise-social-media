from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from . import forms
from .models import Profile
from django.contrib import messages

# Create your views here.

def user_login(request):
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Authentication successfully")
                return HttpResponse("Disabled account")
        return HttpResponse("Invalid login")
    else:
        form = forms.LoginForm()
    return render(request, 'account/login.html', {'form' : form})

@login_required
def dashboard(request):
    return render(request, "account/dashboard.html", {'section' : 'dashboard'})


def register(request):
    if request.method == "POST":
        user_form = forms.UserRegistrationForm(request.POST)
        if user_form.is_valid():
            print("validation passed")
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, "account/register_done.html", {'new_user' : new_user})
        print("validation failed")
    else:
        user_form = forms.UserRegistrationForm()
    return render(request, "account/register.html", {'user_form' : user_form})


@login_required
def edit(request):
    if request.method == "POST":
        user_form = forms.UserEditForm(instance=request.user,
                                       data=request.POST)
        profile_form = forms.ProfileEditForm(instance=request.user.profile,
                                             data=request.POST,
                                             files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated  successfully")
        else:
            messages.error(request, "Error updating your profile")
    else:
        user_form = forms.UserEditForm(instance=request.user)
        profile_form = forms.ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form' : user_form, 'profile_form' : profile_form})



