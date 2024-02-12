from django.urls import path

from dashboard_api.views import (
    TestAPIView,
    RegisterUserAPIView,
)

urlpatterns = [
    path('test/', TestAPIView.as_view(), name='test'),
    path('auth/register/', RegisterUserAPIView.as_view(), name='auth_register'),
]
