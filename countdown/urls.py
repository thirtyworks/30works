from django.urls import path
from .views import countdown
from . import views


urlpatterns = [
    path('', views.countdown, name="countdown"),
]
