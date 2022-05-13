from apis.restaurants import views
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'list', views.RestaurantModelViewSet, basename='restaurant')
router.register(r'menu', views.RestaurantMenuModelViewSet, basename='menu')
urlpatterns = [
    path('', include(router.urls)),
]
