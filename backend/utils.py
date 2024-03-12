from django.contrib.auth.models import User
from django.utils import timezone


def suspend_user(username):
    try:
        user = User.objects.get(username=username)
        user.is_active = False
        user.suspended_at = timezone.now()
        user.save()
        return True, "User suspended successfully"
    except User.DoesNotExist:
        return False, "User does not exist"
