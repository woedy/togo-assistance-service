from django.urls import path

from security_team.api.views.slot_views import set_guard_availability, list_guard_availability

app_name = 'security_team'

urlpatterns = [
    path('set-guard-availability/', set_guard_availability, name="set_guard_availability"),
    path('list-guard-availability/', list_guard_availability, name="list_guard_availability"),

]
