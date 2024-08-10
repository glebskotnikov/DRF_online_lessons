from django.urls import path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, PaymentListAPIView
from users.apps import UsersConfig

app_name = UsersConfig.name

router = DefaultRouter()
router.register("", UserViewSet, basename="users")

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payments-list"),
] + router.urls
