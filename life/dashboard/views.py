from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView, CreateView, ListView, View
from .forms import EventCreationForm, SessionCreationForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from events.models import Event, Ticket, Booking, Session
from events.bookings import consume_ticket
from django.db.models import Sum, Aggregate
from events.bookings import create_session

# Create your views here.

class DashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    This view is for the home page for organizers where they can their own events in a list

    Only users in the Organization group can access it

    It is ordered by -pk, hence displaying the newest events first
    """
    template_name = "dashboard/home.html"
    context_object_name = "events"
    def test_func(self):
        return self.request.user.groups.filter(name="Organization").exists()
    def get_queryset(self):
        return Event.objects.filter(organization = self.request.user.organization).order_by("-pk")

class EventCreationView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Lets organizers create new events 

    Instantiates EventCreationForm which takes in the fields of a new event

    Redirects back to the dashboard home screen on success or failure
    """
    form_class = EventCreationForm
    template_name = "dashboard/event_creation.html"
    #reverse_lazy is used instead of reverse as this is a class attribute and will loaded by python before the urls exist
    success_url = reverse_lazy("dashboard")
    def test_func(self):
        return self.request.user.groups.filter(name="Organization").exists()
    def form_valid(self, form):
        
        form.instance.organization = self.request.user.organization
        return super().form_valid(form)

class SessionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Lets organizers create new sessions for their own events

    The user is first checked to be logged in and then checked if they are an organizer.

    Events which are of kind TICKET can have only one session associated with them wheras SLOT can have multiple

    Instantiates SessionCreationForm which takes in fields required for a new event and checks to make sure the end time of
    an event is not before it's start time
    
    Redirects back to the dashboard home on success or failure
    """
    form_class = SessionCreationForm
    template_name = "dashboard/session_creation.html"
    success_url = reverse_lazy("dashboard")
    def test_func(self):
        return self.request.user.groups.filter(name="Organization").exists()
    def get_event(self):
        #we are fetching the specific Event instance using the URL's kwargs- pk. 
        return get_object_or_404(Event, pk=self.kwargs["pk"], organization=self.request.user.organization)
        #ensures that other organizers cant access any event just by guessing the correct pk in the url (organization=self.request.user.organization)
        #a 404 error will be thrown if they try to
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event"] = self.get_event()
        return context
        #context is a dictionary which will store data from this certain event model
    def form_valid(self, form):
        try:
            create_session(self.get_event(), form)
        except ValueError as e:
            messages.error(self.request, str(e))
        return HttpResponseRedirect(reverse("dashboard"))

class OrgsTicketView(LoginRequiredMixin, UserPassesTestMixin, ListView):
        """
        Lets organizers view every ticket that was bought for one of their events.

        Tickets are listed by newest first
        """
        template_name = "dashboard/org_ticket_list.html"
        context_object_name ="tickets"
        def test_func(self):
                return self.request.user.groups.filter(name="Organization").exists()
        def get_queryset(self):
             #the __ is used to follow a relationship
             return  Ticket.objects.filter(booking__session__event__organization = self.request.user.organization).order_by("-booking__created_at")
             #ordering by negavtive booking date so that it comes in decending order

class TicketConsumeView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Lets organizers mark a particular ticket as consumed

    It accepts POST requests and a ticket can only be marked as consumed 
    if it belongs to that particular organisation's event

    This is enforced in consume_ticket from events/bookings.py, which this view calls

    Redirects to the ticket list on success or failure
    """
    def test_func(self):
        return self.request.user.groups.filter(name="Organization").exists()

    def post(self, request, pk):
        try:
            consume_ticket(request.user.organization, pk)
        except ValueError as e:
            messages.error(request, str(e))
        return HttpResponseRedirect(reverse("org_tickets"))

class AnalyticsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Lets organizers view analytics for all their events

    Checks if the user is logged in and is an organizer
    """
    template_name = "dashboard/analytics.html"
    def test_func(self):
         return self.request.user.groups.filter(name="Organization").exists()
    def get_context_data(self, **kwargs):
        """
        Adds the organizer's analytics to the context 
        """
        #super is used here to call a method of the parent class (that being TemplateView over here as 
        #LoginRequiredMixin and UserPassTestMixin dont have this)
        context = super().get_context_data(**kwargs)
        organization = self.request.user.organization
        tickets = Ticket.objects.filter(booking__session__event__organization = organization)
        bookings = Booking.objects.filter(session__event__organization = organization)
        context["ticketstotal"]=tickets.count()
        context["ticketsactive"] =tickets.filter(status="ACTIVE").count()
        context["ticketsconsumed"] =tickets.filter(status="CONSUMED").count()
        context["bookingstotal"] = bookings.count()
        context["revenue"] = bookings.aggregate(total=Sum("totalprice"))["total"]
        seats = Session.objects.filter(event__organization=organization).aggregate(booked=Sum("seats_booked"), capacity=Sum("capacity"))
        booked = seats["booked"] 
        capacity = seats["capacity"]        
        context["seatsbooked"] = booked
        context["seatscapacity"] = capacity
        context["perevent"] = (bookings.values("session__event__id", "session__event__title").annotate(tickets=Sum("quantity"), revenue=Sum("totalprice")))
        return context

