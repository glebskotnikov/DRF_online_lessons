from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from users.models import User


@shared_task
def send_information_about_course_update(email, course_name):
    """Отправляет сообщение пользователю об обновлении материалов курса"""
    send_mail(
        "Курс обновлен",
        f"Материалы курса ({course_name}) обновлены",
        EMAIL_HOST_USER,
        [email],
    )


@shared_task
def deactivate_inactive_users():
    """Деактивирует неактивных пользователей"""
    month_ago = timezone.now() - timedelta(days=30)
    User.objects.filter(last_login__lte=month_ago).update(is_active=False)
