from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Event, Review, UserEvent, Chat, SuspendedUser, BannedUser

admin.site.register(Event)
admin.site.register(Review)
admin.site.register(UserEvent)
admin.site.register(Chat)


class SuspendedUserInline(admin.StackedInline):
    model = SuspendedUser
    can_delete = False
    verbose_name_plural = "Suspended Users"
    readonly_fields = ["suspended_at"]


class BannedUserInline(admin.StackedInline):
    model = BannedUser
    can_delete = False
    verbose_name_plural = "Banned Users"
    readonly_fields = ["banned_at"]


class UserAdmin(BaseUserAdmin):
    inlines = (
        SuspendedUserInline,
        BannedUserInline,
    )
    actions = ["ban_user", "unban_user", "suspend_user", "unsuspend_user"]

    def ban_user(self, request, queryset):
        for user in queryset:
            banned_user, created = BannedUser.objects.get_or_create(
                user=user, defaults={"reason": "Reason for ban goes here"}
            )
            if created:
                user.is_active = False
                user.save()
                self.message_user(
                    request, f"User {user.username} has been banned successfully."
                )
            else:
                self.message_user(
                    request,
                    f"User {user.username} is already banned.",
                    level=admin.WARNING,
                )

    ban_user.short_description = "Ban selected users"

    # Define unban_user method similarly to ban_user

    def suspend_user(self, request, queryset):
        for user in queryset:
            suspended_user, created = SuspendedUser.objects.get_or_create(
                user=user,
                defaults={
                    "reason": "Reason for suspension goes here",
                    "is_suspended": True,
                },  # 默认设置用户为暂停状态
            )
            if created:
                user.is_active = False
                user.save()
                self.message_user(
                    request, f"User {user.username} has been suspended successfully."
                )
            else:
                self.message_user(
                    request,
                    f"User {user.username} is already suspended.",
                    level=admin.WARNING,
                )

    suspend_user.short_description = "Suspend selected users"

    def unsuspend_user(self, request, queryset):
        for user in queryset:
            try:
                suspended_user = SuspendedUser.objects.get(user=user)
                suspended_user.unsuspend_user()
                self.message_user(
                    request, f"User {user.username} has been unsuspended successfully."
                )
            except SuspendedUser.DoesNotExist:
                self.message_user(
                    request,
                    f"User {user.username} is not suspended.",
                    level=admin.WARNING,
                )

    unsuspend_user.short_description = "Unsuspend selected users"

    def is_banned(self, obj):
        return hasattr(obj, "banneduser")

    is_banned.boolean = True
    is_banned.admin_order_field = "banneduser"

    def is_suspended(self, obj):
        return hasattr(obj, "suspendeduser") and obj.suspendeduser.is_suspended

    is_suspended.boolean = True
    is_suspended.admin_order_field = "suspendeduser__is_suspended"

    list_display = BaseUserAdmin.list_display + (
        "is_banned",
        "is_suspended",
    )
    list_filter = BaseUserAdmin.list_filter + (
        "banneduser",
        "suspendeduser__is_suspended",
    )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class SuspendedUserAdmin(admin.ModelAdmin):
    list_display = [
        "get_username",
        "get_email",
        "reason",
        "suspended_at",
        "unsuspended_at",
        "is_suspended",
    ]
    list_filter = ["suspended_at", "unsuspended_at", "is_suspended", "user__is_active"]

    def get_username(self, obj):
        return obj.user.username

    get_username.admin_order_field = "user__username"

    def get_email(self, obj):
        return obj.user.email

    get_email.admin_order_field = "user__email"
    get_email.short_description = "Email"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(is_active=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(SuspendedUser, SuspendedUserAdmin)
