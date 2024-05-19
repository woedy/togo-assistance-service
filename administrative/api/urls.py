from django.urls import path

from administrative.api.views import get_admin_dashboard

app_name = 'administrative'

urlpatterns = [
    path('get-admin-dashboard/', get_admin_dashboard, name="get_admin_dashboard"),
]
