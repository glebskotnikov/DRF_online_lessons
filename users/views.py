from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.serializers import (PaymentSerializer, UserPublicInfoSerializer,
                               UserSerializer)

from .models import Payment, User
from .services import (convert_rub_to_dollars, create_stripe_price,
                       create_stripe_product, create_stripe_session,
                       retrieve_stripe_session)


@extend_schema(
    tags=["Users"],
    summary="Создание нового пользователя",
)
class UserCreateAPIView(CreateAPIView):
    """Создает нового пользователя."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


@extend_schema(
    tags=["Users"],
    summary="Получение списка всех пользователей",
)
class UserListAPIView(ListAPIView):
    """Выводит список всех пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = []
        for user in queryset:
            if request.user == user:
                serializer = self.get_serializer(user)
            else:
                serializer = UserPublicInfoSerializer(user)
            data.append(serializer.data)
        return Response(data)


@extend_schema(
    tags=["Users"],
    summary="Детальная информация о пользователе",
)
class UserRetrieveAPIView(RetrieveAPIView):
    """Выводит детальную информацию о пользователе."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance:
            serializer = self.get_serializer(instance)
        else:
            serializer = UserPublicInfoSerializer(instance)
        return Response(serializer.data)


@extend_schema(
    tags=["Users"],
    summary="Изменение существующего пользователя",
)
class UserUpdateAPIView(UpdateAPIView):
    """Изменяет существующего пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance:
            return super().update(request, *args, **kwargs)
        else:
            return Response(
                {"message": "You cannot edit other user's profile"}, status=403
            )


@extend_schema(
    tags=["Users"],
    summary="Удаление существующего пользователя",
)
class UserDestroyAPIView(DestroyAPIView):
    """Удаляет существующего пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"message": "You cannot delete other user's profile"}, status=403
            )

    def perform_destroy(self, instance):
        instance.delete()


@extend_schema(
    tags=["Payments"],
    summary="Получение списка всех платежей",
)
class PaymentListAPIView(ListAPIView):
    """Выводит список всех платежей пользователя"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("course", "lesson", "payment_type")
    ordering_fields = ("payment_date",)


@extend_schema(
    tags=["Payments"],
    summary="Создание нового платежа",
)
class PaymentCreateAPIView(CreateAPIView):
    """Создает новый платеж."""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        amount_in_dollars = convert_rub_to_dollars(payment.amount)
        product = create_stripe_product()
        price = create_stripe_price(amount_in_dollars, product)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


@api_view(["GET"])
def retrieve_stripe_session_view(request, session_id):
    """Получает данные о сессии в stripe по её идентификатору и отправляет их в ответе."""
    if request.user.is_authenticated:
        session = retrieve_stripe_session(session_id)
        return Response(session)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
