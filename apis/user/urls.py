from apis.user import views
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('employee', views.EmployeeModelViewSet, basename='employee')

urlpatterns = [
    path('register/', views.UserRegistrationAPIView.as_view(), name="user_register_api"),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/token/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    path('logout/', views.LogoutApiView.as_view(), name='user_logout'),
    path('employee/<int:pk>/update/<str:status>/', views.EmployeeModelViewSet.as_view({"patch": "status_update"})),
    path('', include(router.urls)),
]
