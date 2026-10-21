from django.contrib import admin
from .models import Organization, Wallet, WalletTransaction
from django import forms
from .forms import OrganizationCreationForm
from .customer import createorganisation
# Register your models here.


@admin.register(Organization) #this decorator registers the OrganisationAdmin class with the Organization model
class OrganisationAdmin(admin.ModelAdmin):

    list_display = ("name", 'user')
    def get_form(self, request, obj = None, **kwargs):
        #if obj is none(it doesnt exist) then django will have to swap in the data from OrganisationCreationForm into kwargs
        #if this if statement is false(obj is not None) then django's standard form will be used (showing only the name)
        if obj == None:
            kwargs["form"] = OrganizationCreationForm #stores OrganizationCreationform's configuration
        #super() allows us to use the get_form method from built in django
        return super().get_form(request, obj, **kwargs)

    
    def save_form(self, request, form, change): #change is a boolean variable passed by django to check weather or not the user is creating/editing a record
        obj = super().save_form(request, form, change)  
        if change: #this means change is True hence we just will be editing
            return obj
        #in this case change is False so we will creating
        return createorganisation(
            name=form.cleaned_data["name"],
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )





#registration for WalletTransaction and Wallet
admin.site.register(WalletTransaction)
admin.site.register(Wallet)