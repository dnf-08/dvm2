from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, View
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Event, Booking, Ticket
from .forms import BookingForm
from .models import Event
from .bookings import book_session
from django.contrib import messages
# Create your views here.


class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "events/event_list.html"
    #used to fetch and render all rows 

class BookSessionsView(LoginRequiredMixin, UserPassesTestMixin, View):
    """This view uses BookingForm to take input for the quantity that is to be purchased

       BookingForm is an Integerfield hence anything inputted which is not an integer greater than one doesnt pass. """
    
    def test_func(self):
        return self.request.user.groups.filter(name="Customer").exists()
    def post(self, request, pk):
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                book_session(request.user, pk, form.cleaned_data["quantity"])
            except ValueError as e:
                messages.error(request, str(e))
            else:
                return HttpResponseRedirect(reverse("bookings"))#sends to the bookings page post successful order
        #this else handles when the form turns out invalid
        else:
            messages.error(request, "Enter a valid quantity.")
    
        return HttpResponseRedirect(reverse("home"))


#basic list views to display the bookings and the tickets
class BookingListView(LoginRequiredMixin, UserPassesTestMixin, ListView):

    """This view uses the ListView to display all of the user's bookings

        It orders the bookings by reverse of the booking time"""
    
    template_name = "events/bookings_list.html"
    context_object_name = "bookings"

    def test_func(self):
        return self.request.user.groups.filter(name="Customer").exists()
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by("-created_at")

class TicketListView(LoginRequiredMixin, UserPassesTestMixin, ListView):

    """This view uses ListView to display all of the user's entry passes

        It's order by the reverse of the booking time
        On this page users can see the unique uuid of their bookings."""
    
    template_name = "events/ticket_list.html"
    context_object_name = "tickets"

    def test_func(self):
        return self.request.user.groups.filter(name="Customer").exists()

    def get_queryset(self):
        return Ticket.objects.filter(
            booking__user=self.request.user, status="ACTIVE").order_by("-booking__created_at")