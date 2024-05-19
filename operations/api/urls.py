from django.urls import path
from human_resources.api.views import get_hr_dashboard
from operations.api.views import get_operations_dashboard

app_name = 'operations'

urlpatterns = [
    path('get-operations-dashboard/', get_operations_dashboard, name="get_operations_dashboard"),
]
