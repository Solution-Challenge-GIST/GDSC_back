import dj_rest_auth.views
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accountapp import views
from accountapp.views import UserViewSet

urlpatterns = [
    # Django Rest Auth
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout', dj_rest_auth.views.LogoutView.as_view(), name='logout'),
    path('password/reset', dj_rest_auth.views.PasswordResetView.as_view(), name='password_reset'),
    path('registration', include('dj_rest_auth.registration.urls')),

    path('users/me', UserViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}))
]