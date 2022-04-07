from urllib import request
from .models import Day
from django.contrib.auth import logout
import datetime

def GetDate(request):
    days = Day.objects.last()
    return {"days":days}

def get_latest_day_number(request):
    day = Day.objects.last()
    if day:
        day_number = day.number
    else:
        day_number = 1
    return {"day_number": 1}


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Check if user session is still logged in after user is blocked then force log them out.
        if request.user.is_authenticated and not request.user.is_active:
            logout(request)
        return response