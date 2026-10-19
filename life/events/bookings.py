from django.db import transaction
from django.utils import timezone
from accounts.models import WalletTransaction, Wallet
from .models import Bookings, Session, Tickets

@transaction.atomic
def book_session (user, session_id, quantity):
    wallet =Wallet.objects.select_for_update().get(user = user) #locks the row
    try:
        session = Session.objects.select_for_update().get(pk=session_id)
     #try to lock the session unless the session id is invalid in which case raise ValueError
    except:
        ValueError("this session doesn't exist")

    if session.remaining() < quantity:
        raise ValueError("not enough seats left in this session")
    
    total = session.price * quantity

    if  wallet.balance < total:
        raise ValueError("insufficient funds")

    wallet.balance -= total
    wallet.save()
    session.seats_booked += quantity
    session.save()

    #adds to the debit transaction to the wallet page also
    payment = WalletTransaction.objects.create(wallet = wallet, 
                                            type ="DEBIT",
                                              amount = total,
                                                balance_after = wallet.balance,)

    #create the bookings
    booking = Bookings.objects.create(user = user,
                                      session = session,
                                      quantity = quantity,
                                      totalprice = total,
                                      payment = payment
                                      )
    #generate the tickets using a loop for the amount of quantity of bookings purchased
    for _ in range(quantity):
        Tickets.objects.create(booking=booking)

    return booking
