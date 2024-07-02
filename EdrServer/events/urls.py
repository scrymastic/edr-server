
from django.urls import path
from . import views


urlpatterns = [
    path('events/', views.view_events, name='events'),
    path('events/read_events/', views.read_events, name='read_events'),
    path('events/upload_file/', views.upload_file, name='upload_file'),
    path('events/search_events/', views.search_events, name='search_events'),
    path('events/get_event/', views.get_event, name='get_event'),
    path('events/push_events/', views.push_events, name='push_events'),
]