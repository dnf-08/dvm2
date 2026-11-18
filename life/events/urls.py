from django.urls import path
from . import views

urlpatterns=[
    path("", views.EventListView.as_view(), name="home"), 
    path("sessions/<int:pk>/book/", views.BooksessionsView.as_view(), name="book_session"),
    path("bookings/", views.BookingListView.as_view(), name="bookings"),
    path("tickets/", views.TicketListView.as_view(), name="tickets"),
]