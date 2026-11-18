from django.urls import path
from . import views

urlpatterns=[
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("events/creation/", views.EventCreationView.as_view(), name = "event_creation"),
    path("events/<int:pk>/sessions/add/", views.SessionCreateView.as_view(), name= "session_creation"),
    path("tickets/", views.OrgsTicketView.as_view(), name="org_tickets"),
    path("tickets/<int:pk>/consume/", views.TicketConsumeView.as_view(), name="ticket_consume"),
    path("analytics/", views.AnalyticsView.as_view(), name="analytics"),
]