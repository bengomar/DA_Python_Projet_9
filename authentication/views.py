from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import SignupForm, UploadProfilePhotoForm


def signup_page(request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, "authentication/signup.html", context={"form": form})


def upload_profile_photo(request):
    form = UploadProfilePhotoForm(instance=request.user)
    if request.method == "POST":
        form = UploadProfilePhotoForm(
            request.POST, request.FILES, instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(
        request, "authentication/upload_profile_photo.html", context={"form": form}
    )
