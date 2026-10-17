from django.contrib.auth.models import Group
from django.db import transaction #django databse's transaction tools
from .models import Wallet

#transaction.atomic is used so that if any line fails, everything done so far will get rollbacked
@transaction.atomic
def createcustomer(form):
    user = form.save() #form is from the signup view
    user.groups.add(Group.objects.get(name = "Customer")) #adds the new user to the Customer group created in the migration
    Wallet.objects.create(user = user) #creates a wallet for the use rwith default balance 0
    return user