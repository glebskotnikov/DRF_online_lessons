from django.urls import path
from rest_framework.routers import DefaultRouter

from lms.apps import LmsConfig
from lms.views import (CourseViewSet, LessonCreateAPIView,
                       LessonDestroyAPIView, LessonListAPIView,
                       LessonRetrieveAPIView, LessonUpdateAPIView,
                       SubscriptionAPIView)

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="courses")

urlpatterns = [
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson-create"),
    path("lessons/", LessonListAPIView.as_view(), name="lesson-list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson-get"),
    path(
        "lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson-update"
    ),
    path(
        "lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson-delete"
    ),
    path("subscriptions/", SubscriptionAPIView.as_view(), name="subscriptions"),
] + router.urls
