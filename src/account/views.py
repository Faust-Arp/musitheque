from django.shortcuts import render, redirect

from account.forms import UserRegistrationForm


def signup(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/login")
    else:
        form = UserRegistrationForm()

    return render(request, "account/signup.html", {"form": form})
