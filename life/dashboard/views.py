from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView

# Create your views here.

class DashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "dashboard/home.html"
    def test_func(self):
        return self.request.user.groups.filter(name="Organization").exists()
    