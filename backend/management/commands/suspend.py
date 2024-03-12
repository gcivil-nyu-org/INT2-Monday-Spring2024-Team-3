from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Pause comments and ratings for a user"

    def add_arguments(self, parser):
        parser.add_argument(
            "username",
            type=str,
            help="Username of the user to pause comments and ratings for",
        )

    def handle(self, *args, **kwargs):
        username = kwargs["username"]
        try:
            user = User.objects.get(username=username)

            # 在这里实现暂停评论和评分的逻辑
            # 例如，您可以将用户的评论和评分状态设置为暂停
            user.comments_enabled = False
            user.ratings_enabled = False
            user.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully paused comments and ratings for user {username}"
                )
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"User with username {username} does not exist")
            )
