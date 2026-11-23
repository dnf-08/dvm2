from django.db import models
from django.conf import settings
# Create your models here.

#organization is used to store data about the users and their public names 
class Organization(models.Model):
    """
    This model describes the data associated with organisers

    Organisers are allowed to create new events and hence sessions for those events
    """
    #here name is what will be displayed to the public while user point to django's auth_user table
    name = models.CharField(max_length = 200)
    user = models.OneToOneField( settings.AUTH_USER_MODEL, on_delete= models.CASCADE , related_name="organization" )
    #CASCADE means that when a when a user is deleted, the organisation row corresponding to said user would also be deleted

#wallet is used to store data about the users and their balance
class Wallet(models.Model):
    """
    This model describes the data asssociated with the user's wallet

    It ensures that the user's wallet balance is greater than or equal to zero at all times also
    """
    user = models.OneToOneField( settings.AUTH_USER_MODEL, on_delete= models.CASCADE , related_name="wallet"    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0) #decimal used as float is not precise

    #here class Meta is used to check that all wallet balances will be greater than 0, 
    #this is done using the Q object( which is used to wrap a condition) (like WHERE in sql)
    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(balance__gte= 0), name="wallet_balance_gte0"
            )           
        ]
    def __str__(self):
        return f"{self.user.username}'s wallet has balance {self.balance}"  
    
#wallet transaction is used to manage the transaction whether its credit or debit and the amount
class WalletTransaction(models.Model):
    """This model describes each transaction which occurs by the user
    
        When the user gains money its credit and when they lose money its labeled as debit.
    """
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name="transactions")
    wchoices = [("CREDIT", "Credit"), ("DEBIT", "Debit")]
    type = models.CharField(max_length= 10, choices= wchoices)
    amount =models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wallet.user} has a transaction of type: {self.type}"