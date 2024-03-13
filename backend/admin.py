# admin.py

from django.contrib import admin
from .models import Event, Review, UserEvent, Chat, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

admin.site.register(Event)
admin.site.register(Review)
admin.site.register(UserEvent)
admin.site.register(Chat)
admin.site.register(UserProfile)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "UserProfile"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    actions = ["ban_users", "suspend_users", "unban_users"]

    def ban_users(self, request, queryset):
        queryset.update(userprofile__is_banned=True)

    ban_users.short_description = "Ban selected users"

    def suspend_users(self, request, queryset):
        # Here you'd set is_suspended to True and set the suspension_end_date accordingly
        pass

    suspend_users.short_description = "Suspend selected users"

    def unban_users(self, request, queryset):
        queryset.update(userprofile__is_banned=False)

    unban_users.short_description = "Unban selected users"


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
