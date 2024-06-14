
from django.urls import path
from . import views

urlpatterns = [
    path('api/receive_events/', views.receive_events, name='receive_events'),
]