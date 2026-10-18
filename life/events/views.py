from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.views.generic import ListView, DetailView
from .models import Event
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