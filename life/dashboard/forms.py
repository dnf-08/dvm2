from django import forms
from events.models import Event, Session

class EventCreationForm(forms.ModelForm):
    """
    Used by an organization to create new events

    instatiated by EventCreationView from dashboard/views.py
    """
    class Meta:
        model = Event
        fields= ["title", "description","kind","venue"]

class SessionCreationForm(forms.ModelForm):
    """
    Used to create new session for a given event by an organization

    instantiated by SessionCreationView from dashboard/views.py

    It also 'cleans' the data to make sur ethat the start time is before the end time
    """
    class Meta:
        model = Session
        fields =["start_time", "end_time", "capacity", "price"]
        widgets ={
            #this makes it so there iss a widget which allows the organisers to choose the dat and time of starting via picker
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}), 
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def clean(self):
        """checks if the start time is before the end time"""
        cdata = super().clean()
        start_time = cdata.get("start_time")
        end_time = cdata.get("end_time")
        if start_time and end_time and end_time <= start_time:
            raise forms.ValidationError("end time must be after start time")
        return cdata