from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView,SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('stocks/', include('stocks.urls')),
    path('transactions/', include('transactions.urls')),
    path('', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
