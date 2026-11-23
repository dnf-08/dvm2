from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.db import transaction #django databse's transaction tools
from .models import Wallet, WalletTransaction,Organization

#transaction.atomic is used so that if any line fails, everything done so far will get rollbacked
@transaction.atomic
def createcustomer(form):
    """
    This is used to create new customers by adding them to the Customer group
    and assign wallet to said customer, it is called by the signup view from accounts/views.py

    """
    user = form.save() #form is from the signup view
    user.groups.add(Group.objects.get(name = "Customer")) #adds the new user to the Customer group created in the migration
    Wallet.objects.create(user = user) #creates a wallet for the use rwith default balance 0
    return user

@transaction.atomic
def creditwallet(user, amount):
    """
    Used to add money to the user's wallet, it is called by AddMoneyView from accounts/views.py

    The inputted amount if also checked to be positive
    """
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
    """
    Used to create new organisations

    It creates a new django User and adds the Organization group to it. It is given a username and a hashed password
    """
    user = get_user_model().objects.create_user(username= username, password= password)
    user.groups.add(Group.objects.get(name="Organization"))
    return Organization.objects.create(user = user, name =name)

