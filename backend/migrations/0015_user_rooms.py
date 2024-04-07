# Generated by Django 4.0.2 on 2024-04-03 17:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("backend", "0014_room3_chatroom3"),
    ]

    operations = [
        migrations.CreateModel(
            name="user_rooms",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "room_joined",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="room_joined",
                        to="backend.room3",
                    ),
                ),
                (
                    "user_detail",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_detail",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
