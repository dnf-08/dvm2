from django.contrib import admin
from .models import Session, Event

# Register your models here.

class SessionInline(admin.TabularInline):
    model = Session


class EventAdmin(admin.ModelAdmin):
    inlines = [SessionInline]

admin.site.register(Event, EventAdmin)