"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts import views as account_views
from events import views as event_views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('admin/', admin.site.urls),

    path("accounts/signup/", account_views.signup, name = "signup"),
    path("accounts/login/", auth_views.LoginView.as_view(), name = "login"), #for class based views .as_view is used
    path("accounts/logout/",  auth_views.LogoutView.as_view(), name = "logout"),

    path("", event_views.EventListView.as_view(), name="home"), 

    path("accounts/wallet", account_views.WalletView.as_view(), name= "wallet"),
    path("accounts/wallet/add/", account_views.AddMoneyView.as_view(), name="add_money"),
    path("sessions/<int:pk>/book/", event_views.BooksessionsView.as_view(), name="book_session"),

    path("bookings/", event_views.BookingListView.as_view(), name="bookings"),
    path("tickets/", event_views.TicketListView.as_view(), name="tickets"),

    
]
