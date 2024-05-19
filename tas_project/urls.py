"""
URL configuration for tas_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from accounts.api.custom_jwt import CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/accounts/', include('accounts.api.urls', 'accounts_api')),
    path('api/clients/', include('clients.api.urls', 'clients_api')),
    path('api/bookings/', include('bookings.api.urls', 'bookings_api')),
    path('api/secretary/', include('secretary.api.urls', 'secretary_api')),
    path('api/reports/', include('reports.api.urls', 'reports_api')),

    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),

]
