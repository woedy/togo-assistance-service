from django.urls import path

from billing.api.views import get_billing_dashboard
from human_resources.api.views import get_hr_dashboard

app_name = 'billing'

urlpatterns = [
    path('get-billing-dashboard/', get_billing_dashboard, name="get_billing_dashboard"),
]
