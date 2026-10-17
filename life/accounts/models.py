from django.db import models
from django.conf import settings
# Create your models here.

#organization is used to store data about the users and their public names 
class Organization(models.Model):
    #here name is what will be displayed to the public while user point to django's auth_user table
    name = models.CharField(max_length = 200)
    user = models.OneToOneField( settings.AUTH_USER_MODEL, on_delete= models.CASCADE , related_name="organization" )
    #CASCADE means that when a when a user is deleted, the organisation row corresponding to said user would also be deleted

#wallet is used to store data about the users and their balance
class Wallet(models.Model):
    user = models.OneToOneField( settings.AUTH_USER_MODEL, on_delete= models.CASCADE , related_name="wallet" )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0) #decimal used as float is not precise

    #here class Meta is used to check that all wallet balances will be greater than 0, 
    #this is done using the Q object( which is used to wrap a function) (like WHERE in sql)
    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(balance__gte= 0), name="wallet_balance_gte0"
            )           
        ]

#wallet transaction is used to manage the transaction whether its credit or debit and the amount
class WalletTransaction(models.Model):
    type = models.CharField(max_length= 10)#is it credit or debit || maybe add set options later
    amount =models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2, default=0)
