"""Views for core app."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def dashboard(request: HttpRequest) -> HttpResponse:
    """Landing page showing resumes and JDs."""
    return render(request, "core/dashboard.html")
