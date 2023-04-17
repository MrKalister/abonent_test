from django.urls import include, path
from rest_framework import routers

from .views import AbonentViewSet, LimitViewSet, Upload

v1_router = routers.DefaultRouter()
v1_router.register('abonents', AbonentViewSet, basename='abonent')
v1_router.register('limits', LimitViewSet, basename='limit')


urlpatterns = [
    path('', include(v1_router.urls)),
    # для управления пользователями в Django
    path('auth/', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами
    path('auth/', include('djoser.urls.jwt')),
    # Эндпоинт для массовой загрузки
    path('upload/', Upload.as_view())
]
