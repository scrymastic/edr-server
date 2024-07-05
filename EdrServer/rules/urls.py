from django.urls import path
from . import views


urlpatterns = [
    path('rules/', views.view_rules, name='rules'),
    path('rules/view_rule/<str:rule_id>', views.view_rule, name='view_rule'),
    path('rules/update_rule/', views.update_rule, name='update_rule'),
    path('rules/copy_rule/<str:rule_id>', views.copy_rule, name='copy_rule'),
    path('rules/search_rules/', views.search_rules, name='search_rules'),
    path('rules/add_rule/', views.add_rule, name='add_rule'),
    path('rules/delete_rule/', views.delete_rule, name='delete_rule'),
    path('rules/toggle_rule/', views.toggle_rule, name='toggle_rule'),
]