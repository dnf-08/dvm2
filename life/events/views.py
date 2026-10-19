from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, View
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Event, Bookings, Tickets
from .forms import BookingForm
from .models import Event
from .bookings import book_session
from django.contrib import messages
# Create your views here.


class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "events/event_list.html"
    #used to fetch and render all rows 

'''can implement template later to display the details of all events
class EventDetailView(LoginRequiredMixin, DetailView):
    model  = Event
    template_name = "events/event_detail.html"
    #used to fetch only a single row via its primary key(pk)
'''

class BooksessionsView(LoginRequiredMixin, UserPassesTestMixin, View):
    
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
    template_name = "events/bookings_list.html"
    context_object_name = "bookings"

    def test_func(self):
        return self.request.user.groups.filter(name="Customer").exists()
    def get_queryset(self):
        return Bookings.objects.filter(user=self.request.user).order_by("-created_at")

class TicketListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "events/ticket_list.html"
    context_object_name = "tickets"

    def test_func(self):
        return self.request.user.groups.filter(name="Customer").exists()

    def get_queryset(self):
        return Tickets.objects.filter(
            booking__user=self.request.user, status="ACTIVE").order_by("-booking__created_at")