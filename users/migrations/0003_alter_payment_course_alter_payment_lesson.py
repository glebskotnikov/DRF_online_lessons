# Generated by Django 5.0.7 on 2024-08-10 21:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lms", "0002_alter_lesson_link"),
        ("users", "0002_payment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="course",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="lms.course",
                verbose_name="оплаченный курс",
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="lesson",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="lms.lesson",
                verbose_name="оплаченный урок",
            ),
        ),
    ]
