from django.urls import path
from .views import UserRegistrationView, NotificationViewset,login,register_view,login_view,dashboard
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register-api/', UserRegistrationView.as_view(), name= 'register-api'),
    path('register/', register_view, name='register'),
    path('login-api/', login.as_view(), name='login-api'),
    path('login/', login_view, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/notifications/', NotificationViewset.as_view({'get': 'list', 'post': 'perform_create'}), name='notifications'),
    path('dashboard/', dashboard, name='dashboard'),
]
