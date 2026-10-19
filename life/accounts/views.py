from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.views.generic import FormView, ListView
#LoginRequiredMixin ensures a user is logged in before accessing the view (checks if it's authenticated)
#UsedPassesTestMixin will check if the user passes the test_func which is defined
from django.urls import reverse_lazy 
#reverse lazy will create an object and resolve the string later unlike reverse, this is useful as django wouldnt be finished "reading" urls.py yet

from .forms import AddMoneyForm
from .models import WalletTransaction
from .customer import createcustomer, creditwallet
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

#---------------wallet views------------------------------------
class WalletView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "accounts/wallet.html"
    context_object_name = "transactions"
    def test_func(self):
        return self.request.user.groups.filter(name="Customer").exists() #checks if the user belongs to the customer group
    
    def get_queryset(self):
        return WalletTransaction.objects.filter(wallet__user=self.request.user).order_by("-created_at")
    #displays all the transactions in decending order of creation date

class AddMoneyView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = AddMoneyForm
    template_name = "accounts/add_money.html"
    success_url = reverse_lazy("wallet")

    def test_func(self):
        return self.request.user.groups.filter(name="Customer").exists()

    def form_valid(self, form):
        creditwallet(self.request.user, form.cleaned_data["amount"])
        return super().form_valid(form)