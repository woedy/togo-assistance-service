

from django.conf import settings
from django.conf.urls.static import static
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

    path('api/commercial/', include('commercial.api.urls', 'commercial_api')),
    path('api/logistics/', include('logistics.api.urls', 'logistics_api')),
    path('api/security-team/', include('security_team.api.urls', 'security_team_api')),
    path('api/operations/', include('operations.api.urls', 'operations_api')),

    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),

]


if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)