from django.db import models
from django.conf import settings
import uuid
# Create your models here.

#event model is used to describe the details of an event
class Event(models.Model):
    #import the organization model from accounts as a foreign key for the event model
    organization = models.ForeignKey("accounts.Organization", on_delete=models.CASCADE, related_name = "events")
    title = models.CharField(max_length = 50)
    description = models.TextField
    kind = models.CharField(max_length = 10) #what kind of event is it? ticket or slot || maybe add set options later
    venue =models.CharField(max_length=50)


#a session is a book-able occerance of a certain event
class Session(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="sessions")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField() 
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    seats_booked = models.IntegerField(default=0)
    #here class Meta is being used to ensure that seat booked will never be greater than capacity for the event.
    #this is done using the Q object(which is used to wrap a function) 
    #and F(which references the value of the column of the row being looked at)
    class Meta:
        constraints= [
            models.CheckConstraint(condition = models.Q(seats_booked__lte= models.F("capacity")), 
            name = "seat_booked_lte")
            ]

    def remaining(self):
            return self.capacity - self.seats_booked

#bookings model is used to implement a system where users can purchase a certain session involing a wallet transaction
class Bookings(models.Model):
     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="bookings")#each user can have multiple bookings
     session = models.ForeignKey(Session, on_delete = models.PROTECT, related_name= "bookings" )
     quantity = models.IntegerField()
     totalprice = models.DecimalField(max_digits=10, decimal_places=2, default=0)
     payment = models.OneToOneField("accounts.WalletTransaction", null = True, blank=True, 
                                    on_delete= models.PROTECT, related_name="bookings")
     #null=True means that that this field can be empty and blank means it's accetable to submit this field as empty
     #PROTECT is used over here to ensure that any session which has a booking can't be delete, 

     created_at = models.DateTimeField(auto_now_add=True) #auto_now_add will add the time the booking was made automatically


#the tickets model gives one unit which gives admission to an event
class Tickets(models.Model):
    status_choices = [("ACTIVE", "Active"),("CONSUMED", "Consumed"),] #[done like this cause its stored as (value stored in db, value shown to user)]
    booking = models.ForeignKey(Bookings, on_delete=models.CASCADE, related_name="tickets")#CASCADE is used to ensure that when a booking is delted it's corresponding tickets would also be deleted
    ticketcode = models.UUIDField(default =uuid.uuid4) #uuid will generate a random code for each ticket. uuid4 is completely random
    status = models.CharField(max_length=10, choices=status_choices, default="ACTIVE")
