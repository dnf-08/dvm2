from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, FormView, CreateView, ListView
from .forms import EventCreationForm, SessionCreationForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from events.models import Event
# Create your views here.

class DashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "dashboard/home.html"
    context_object_name = "events"
    def test_func(self):
        return self.request.user.groups.filter(name="Organization").exists()
    def get_queryset(self):
        return Event.objects.filter(organization = self.request.user.organization).order_by("-pk")

class EventCreationView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = EventCreationForm
    template_name = "dashboard/event_creation.html"
    success_url = reverse_lazy("dashboard")
    def test_func(self):
        return self.request.user.groups.filter(name="Organization").exists()
    def form_valid(self, form):
        
        form.instance.organization = self.request.user.organization
        return super().form_valid(form)

class SessionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
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
        form.instance.event = self.get_event()
        return super().form_valid(form)