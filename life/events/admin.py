from django.contrib import admin
from .models import Session, Event, Booking, Ticket

# Register your models here.

class SessionInline(admin.TabularInline):
    model = Session

class EventAdmin(admin.ModelAdmin):
    inlines = [SessionInline]

admin.site.register(Event, EventAdmin)
admin.site.register(Booking)
admin.site.register(Ticket) 