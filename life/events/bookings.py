from django.db import transaction
from django.utils import timezone
from accounts.models import WalletTransaction, Wallet
from .models import Booking, Session, Ticket, Event

@transaction.atomic
def book_session (user, session_id, quantity):
    """
    This is used for booking a session of an event

    In this transaction, the user's wallet balance must pass particular tests before the payment goes through.

    The process of updating the wallet,creating a booking and generating the tickets
    is wrapped in one transaction so if anything fails the whole thing will get rollbacked.
    """
    wallet =Wallet.objects.select_for_update().get(user = user) #locks the row
    try:
        session = Session.objects.select_for_update().get(pk=session_id)
     #try to lock the session unless the session id is invalid in which case raise ValueError
    except Session.DoesNotExist:
        raise ValueError("this session doesn't exist")
    
    if session.start_time <= timezone.now():
        raise ValueError("this session has already started")
    
    if session.remaining() < quantity:
        raise ValueError("not enough seats left in this session")
    
    total = session.price * quantity

    if  wallet.balance < total:
        raise ValueError("insufficient funds, please go to the wallet tab and add funds")

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
    booking = Booking.objects.create(user = user,
                                      session = session,
                                      quantity = quantity,
                                      totalprice = total,
                                      payment = payment
                                      )
    #generate the tickets using a loop for the amount of quantity of bookings purchased
    for _ in range(quantity):
        Ticket.objects.create(booking=booking)

    return booking



@transaction.atomic
def consume_ticket(organization, ticket_id):
    """
    Used to mark used tickets as consumed so they cant be reused.
    """
    try:
        ticket = Ticket.objects.select_for_update(of=("self",)).get(pk=ticket_id, booking__session__event__organization=organization)
    except Ticket.DoesNotExist:
        raise ValueError("That ticket does not exist.")

    if ticket.status != "ACTIVE":
        raise ValueError("This ticket has already been consumed")
    ticket.status = "CONSUMED"
    ticket.save()
    return ticket

@transaction.atomic
def create_session(event, form):
    """
    Used to create sessions of a particular event
    """
    event = Event.objects.select_for_update().get(pk = event.pk)
    if event.kind == 'TICKET' and event.sessions.exists():
        raise ValueError("Ticketed events only occur once")
    form.instance.event = event
    return form.save()
