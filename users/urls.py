from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (PaymentCreateAPIView, PaymentListAPIView,
                         UserCreateAPIView, UserDestroyAPIView,
                         UserListAPIView, UserRetrieveAPIView,
                         UserUpdateAPIView, retrieve_stripe_session_view)

app_name = UsersConfig.name

urlpatterns = [
    # users
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("", UserListAPIView.as_view(), name="user-list"),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="user-get"),
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="user-update"),
    path("<int:pk>/delete/", UserDestroyAPIView.as_view(), name="user-delete"),
    # payments
    path("payments/", PaymentListAPIView.as_view(), name="payments-list"),
    path("payments/create", PaymentCreateAPIView.as_view(), name="payments-create"),
    path(
        "stripe_session/<str:session_id>/",
        retrieve_stripe_session_view,
        name="retrieve_stripe_session",
    ),
    # token
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]
