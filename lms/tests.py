from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(
            name="Django test course", description="test course", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="Test lesson",
            course=self.course,
            description="test lesson",
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_create(self):
        url = reverse("lms:lesson-create")
        data = {
            "name": "New Lesson",
            "course": self.course.id,
            "description": "new lesson",
            "link": "http://youtube.com/video1",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Lesson")

    def test_lesson_read(self):
        url = reverse("lms:lesson-get", kwargs={"pk": self.lesson.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test lesson")

    def test_lesson_update(self):
        url = reverse("lms:lesson-update", kwargs={"pk": self.lesson.pk})
        data = {
            "name": "Updated Lesson",
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Updated Lesson")

    def test_lesson_delete(self):
        url = reverse("lms:lesson-delete", kwargs={"pk": self.lesson.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_lesson_list(self):
        url = reverse("lms:lesson-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "link": self.lesson.link,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "image": None,
                    "course": self.lesson.course.pk,
                    "owner": self.user.id,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="tester@sky.pro")
        self.course = Course.objects.create(
            name="Django test course", description="test course", owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_subscription(self):
        url = reverse("lms:subscriptions")
        data = {"course_id": self.course.id}
        # Подписка на курс
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка добавлена")

        # Отписка от курса
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка удалена")


class CourseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(
            name="Django test course", description="test course", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="Test lesson",
            course=self.course,
            description="test lesson",
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_course_create(self):
        url = reverse("lms:courses-list")
        data = {
            "name": "New Course",
            "description": "A new exciting course",
            "owner": self.user.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Course")

    def test_course_retrieve(self):
        url = reverse("lms:courses-detail", kwargs={"pk": self.course.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.course.name)

    def test_course_update(self):
        url = reverse("lms:courses-detail", kwargs={"pk": self.course.id})
        data = {"name": "Updated Course"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Course")

    def test_delete_course(self):
        url = reverse("lms:courses-detail", kwargs={"pk": self.course.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_list_courses(self):
        url = reverse("lms:courses-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 4,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "name": self.course.name,
                    "image": None,
                    "description": self.course.description,
                    "owner": self.user.id,
                    "is_subscribed": None,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
