from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson, Subscription
from lms.paginations import CustomPagination
from lms.serializers import CourseDetailSerializer, CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsNotModer, IsOwner


@extend_schema(tags=["Courses"])
@extend_schema_view(
    list=extend_schema(
        summary="Получение списка всех курсов",
    ),
    create=extend_schema(
        summary="Создание нового курса",
    ),
    update=extend_schema(
        summary="Изменение существующего курса",
    ),
    partial_update=extend_schema(summary="Краткое описание частичного изменения"),
    retrieve=extend_schema(
        summary="Детальная информация о курсе",
    ),
    destroy=extend_schema(
        summary="Удаление курса",
    ),
)
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all().order_by("id")
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (IsAuthenticated, IsNotModer)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsAuthenticated, IsModer | IsOwner)
        elif self.action == "destroy":
            self.permission_classes = (IsAuthenticated, IsOwner & IsNotModer)
        return super().get_permissions()


@extend_schema(
    tags=["Lessons"],
    summary="Создание нового урока",
)
class LessonCreateAPIView(CreateAPIView):
    """Создает новый урок."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsNotModer)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


@extend_schema(
    tags=["Lessons"],
    summary="Получение списка всех уроков",
)
class LessonListAPIView(ListAPIView):
    """Выводит список всех уроков."""

    queryset = Lesson.objects.all().order_by("id")
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


@extend_schema(
    tags=["Lessons"],
    summary="Детальная информация об уроке",
)
class LessonRetrieveAPIView(RetrieveAPIView):
    """Выводит детальную информацию об уроке."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


@extend_schema(
    tags=["Lessons"],
    summary="Изменение существующего урока",
)
class LessonUpdateAPIView(UpdateAPIView):
    """Изменяет существующий урок."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


@extend_schema(
    tags=["Lessons"],
    summary="Удаление существующего урока",
)
class LessonDestroyAPIView(DestroyAPIView):
    """Удаляет существующий урок."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner & IsNotModer)


@extend_schema(
    tags=["Subscriptions"],
    summary="Добавление или удаление статуса подписки",
)
class SubscriptionAPIView(APIView):
    """Добавляет или удаляет статус подписки"""

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)

        subscription, created = Subscription.objects.get_or_create(
            user=user, course=course_item
        )

        if not created:
            subscription.delete()
            message = "Подписка удалена"
        else:
            message = "Подписка добавлена"

        return Response({"message": message}, status=status.HTTP_200_OK)
