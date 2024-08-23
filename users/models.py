from django.contrib.auth.models import AbstractUser
from django.db import models

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
        "lms.Course",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="оплаченный курс",
    )
    lesson = models.ForeignKey(
        "lms.Lesson",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="оплаченный урок",
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="сумма оплаты"
    )
    PAYMENT_TYPE_CHOICES = [
        ("cash", "Cash"),
        ("transfer", "Bank Transfer"),
        ("stripe", "Stripe"),
    ]
    payment_type = models.CharField(
        max_length=10, choices=PAYMENT_TYPE_CHOICES, verbose_name="способ оплаты"
    )

    session_id = models.CharField(max_length=255, verbose_name="id сессии", **NULLABLE)
    link = models.URLField(max_length=400, verbose_name="ссылка на оплату", **NULLABLE)

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"
        ordering = ["payment_date"]

    def __str__(self):
        return f"{self.user} - {self.amount} ({self.payment_date})"
