from django.contrib import admin
from .models import Organization, Wallet, WalletTransaction

# Register your models here.
admin.site.register(Organization) 

admin.site.register(WalletTransaction)
admin.site.register(Wallet)