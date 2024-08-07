
from django.urls import path
from . import views


urlpatterns = [
    path('alerts/', views.view_alerts, name='alerts'),
    path('alerts/get_alert/', views.get_alert, name='get_alert'),
    path('alerts/search_alerts/', views.search_alerts, name='search_alerts'),
]

