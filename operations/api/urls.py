from django.urls import path
from human_resources.api.views import get_hr_dashboard
from operations.api.views import get_operations_dashboard, update_role

app_name = 'operations'

urlpatterns = [
    path('get-operations-dashboard/', get_operations_dashboard, name="get_operations_dashboard"),
    path('update-role/', update_role, name="update_role"),
]
