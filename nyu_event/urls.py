"""
URL configuration for nyu_event project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from backend import views

urlpatterns = (
    [
        path("user/", include("backend.urls")),
        path("admin/", admin.site.urls),
        path(
            "reset_password/",
            auth_views.PasswordResetView.as_view(template_name="reset_password.html"),
            name="reset_password",
        ),
        path(
            "reset_password_sent/",
            auth_views.PasswordResetDoneView.as_view(
                template_name="reset_password_sent.html"
            ),
            name="password_reset_done",
        ),
        path(
            "reset/<uidb64>/<token>/",
            auth_views.PasswordResetConfirmView.as_view(template_name="reset.html"),
            name="password_reset_confirm",
        ),
        path(
            "reset_password_complete/",
            auth_views.PasswordResetCompleteView.as_view(
                template_name="reset_password_complete.html"
            ),
            name="password_reset_complete",
        ),
        path(
            "pusher/auth", views.pusher_config.pusher_authentication, name="pusher_auth"
        ),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + [
        re_path(
            r".*", views.base.not_found_page, name="not_found"
        ),  # only if the above routes don't trigger a match
    ]
)
