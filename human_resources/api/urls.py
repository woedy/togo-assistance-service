from django.urls import path
from human_resources.api.views import get_hr_dashboard

app_name = 'human_resources'

urlpatterns = [
    path('get-hr-dashboard/', get_hr_dashboard, name="get_hr_dashboard"),
]
