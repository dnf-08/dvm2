from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .signup_customer import createcustomer
# Create your views here.


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = createcustomer(form)
            login(request, user)
            return redirect("home") #login the new user and send them to the home page
    else:
        form = UserCreationForm() #a normal page will get a blank form
    return render(request, "registration/signup.html", {"form": form})