from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.db import transaction #django databse's transaction tools
from .models import Wallet, WalletTransaction,Organization

#transaction.atomic is used so that if any line fails, everything done so far will get rollbacked
@transaction.atomic
def createcustomer(form):
    user = form.save() #form is from the signup view
    user.groups.add(Group.objects.get(name = "Customer")) #adds the new user to the Customer group created in the migration
    Wallet.objects.create(user = user) #creates a wallet for the use rwith default balance 0
    return user

@transaction.atomic
def creditwallet(user, amount):
    if amount <= 0:
        raise ValueError("amount can't be negatve")
    wallet = Wallet.objects.select_for_update().get(user = user) #fetch the user's wallet data and lock the row until this transaction is done
    #the lock system is reqd over here as if two credits occur at once, they both would read the initial value and hence wouldnt giver a correct final value, 
    #with only have the first request is commited then only the second will also be credited to the wallet
    wallet.balance += amount
    wallet.save()
    return WalletTransaction.objects.create(wallet = wallet, 
                                            type ="credit",
                                              amount = amount,
                                                balance_after = wallet.balance,)


@transaction.atomic
def createorganisation(name, username ,password):
    user = get_user_model().objects.create_user(username= username, password= password)
    user.groups.add(Group.objects.get(name="Organization"))
    return Organization.objects.create(user = user, name =name)

