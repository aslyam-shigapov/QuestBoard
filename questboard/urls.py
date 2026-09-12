from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),

    # allauth (соцлогин: GitHub, Яндекс)
    path('accounts/', include('allauth.urls')),

    # dj-rest-auth (REST для логина/регистрации)
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),

    # Веб-страницы
    path('users/', include('users.urls', namespace='users')),
    path('', include('boards.urls', namespace='boards')),
    path('quests/', include('quests.urls', namespace='quests')),

    # API
    path('api/boards/', include('boards.api_urls', namespace='boards_api')),
    path('api/quests/', include('quests.api_urls', namespace='quests_api')),
    path('api/profile/', include('users.api_urls', namespace='users_api')),

    # Swagger / Redoc
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)