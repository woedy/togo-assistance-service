from django.urls import path

from reports.api.views import add_internal_report

app_name = 'reports'

urlpatterns = [
    path('add-internal-report/', add_internal_report, name="add_internal_report"),
]
