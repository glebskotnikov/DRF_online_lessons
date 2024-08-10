from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="почта")

    phone = models.CharField(max_length=35, verbose_name="телефон", **NULLABLE)
    city = models.CharField(max_length=35, verbose_name="город", **NULLABLE)
    avatar = models.ImageField(upload_to="users/", verbose_name="аватар", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        ordering = ["email"]

    def __str__(self):
        return self.email


class Payment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="пользователь",
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="дата оплаты")
    course = models.ForeignKey(
        Course, null=True, on_delete=models.SET_NULL, verbose_name="оплаченный курс"
    )
    lesson = models.ForeignKey(
        Lesson, null=True, on_delete=models.SET_NULL, verbose_name="оплаченный урок"
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="сумма оплаты"
    )
    PAYMENT_TYPE_CHOICES = [
        ("cash", "Cash"),
        ("transfer", "Bank Transfer"),
    ]
    payment_type = models.CharField(
        max_length=10, choices=PAYMENT_TYPE_CHOICES, verbose_name="способ оплаты"
    )

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"
        ordering = ["payment_date"]

    def __str__(self):
        return f"{self.user} {self.payment_date}"
