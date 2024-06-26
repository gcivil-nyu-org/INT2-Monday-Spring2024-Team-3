# Generated by Django 5.0.2 on 2024-04-05 17:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0013_review_liked_by"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="reply_count",
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name="ReplyToReview",
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
                ("reply_text", models.TextField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "fromUser",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replies_from",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "review",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replies",
                        to="backend.review",
                    ),
                ),
                (
                    "toUser",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replies_to",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
