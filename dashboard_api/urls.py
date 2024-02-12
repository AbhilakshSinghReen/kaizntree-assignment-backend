from django.urls import path
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)

from dashboard_api.views import (
    TestAPIView,
    RegisterUserAPIView,
    ItemCategoryGenericAPIView,
)

urlpatterns = [
    path('test/', TestAPIView.as_view(), name='test'),

    # Auth
    path('auth/register/', RegisterUserAPIView.as_view(), name='auth_register'),
    path('auth/login/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('auth/logout/', TokenBlacklistView.as_view(), name="token_blacklist"),

    ###
    path('item-categories/', ItemCategoryGenericAPIView.as_view(), name="item_categories"),
    path('item-categories/<int:id>/', ItemCategoryGenericAPIView.as_view(), name="item_categories_with_pk"),
]
