from django.db import models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name="название курса")
    image = models.ImageField(
        upload_to="courses/image", verbose_name="превью курса", **NULLABLE
    )
    description = models.TextField(verbose_name="описание курса")

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, related_name="lessons", on_delete=models.CASCADE, verbose_name="курс"
    )
    name = models.CharField(max_length=150, verbose_name="название урока")
    description = models.TextField(verbose_name="описание урока")
    image = models.ImageField(
        upload_to="lessons/image", verbose_name="превью урока", **NULLABLE
    )
    link = models.CharField(max_length=250, verbose_name="ссылка на видео", **NULLABLE)

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
