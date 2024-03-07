from django.test import TestCase, Client
from django.urls import reverse
from backend.models import Event, User
from django.core import mail
from django.contrib.messages import get_messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import datetime


class EventViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@nyu.edu", password="12345Password!"
        )
        self.event = Event.objects.create(
            title="Spamalot",
            category="Musical, Comedy, Revival, Broadway",
            description="Lovingly ripped from the film classic",
            open_date=datetime.date(2023, 11, 16),
            close_date=datetime.date(2023, 10, 31),
            location="St. James Theatre, 246 West 44th Street, Between Broadway and 8th Avenue",
            availability="available",
            external_link="http://www.broadway.org/shows/details/spamalot,812",
            image_url="https://www.broadway.org/logos/shows/spamalot-2023.jpg",
            avg_rating=0,  # Assuming initial avg_rating
        )

        self.event_id = self.event.pk
        self.category = self.event.category

    def test_index_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_event_detail_view(self):
        response = self.client.get(reverse("event_detail", args=(self.event_id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "event_detail.html")

        response = self.client.get(reverse("event_detail", args=(9999,)))
        self.assertEqual(response.status_code, 404)

    def test_search_results_view(self):
        response = self.client.get(
            reverse("search_results") + "?search_events=Spamalot"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search_results.html")

        # Test the search results with a term that does not match
        response = self.client.get(
            reverse("search_results") + "?search_events=Nonexistent"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search_results.html")

    def test_index_with_categories_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_events_by_category_view(self):
        response = self.client.get(reverse("events_by_category", args=(self.category,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events_by_category.html")

        response = self.client.get(reverse("events_by_category", args=("Nonexistent",)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "events_by_category.html")

    def test_register_user_view(self):
        form_data = {
            "username": "newuser@nyu.edu",
            "email": "newuser@nyu.edu",
            "password1": "testpassworD1!",
            "password2": "testpassworD1!",
        }
        response = self.client.post(reverse("register"), form_data)

        # Check redirection to login page after registration
        self.assertRedirects(response, reverse("login"))

        # Check if an email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Activate your user account")

        # Check if user is not active before activation
        new_user = User.objects.get(username="newuser@nyu.edu")
        self.assertFalse(new_user.is_active)

    def test_account_activation(self):
        # Prepare the token and uid
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        # Activation with correct token
        response = self.client.get(reverse("activate", args=(uid, token)))
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertRedirects(response, reverse("login"))

        # Deactivate the user for the test
        self.user.is_active = False
        self.user.save()

        # Activation with incorrect token
        response = self.client.get(reverse("activate", args=(uid, "wrong-token")))
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_login_user_view(self):
        # Test login with correct credentials
        response = self.client.post(
            reverse("login"),
            {"username": "testuser@nyu.edu", "password": "12345Password!"},
        )
        self.assertRedirects(response, reverse("index"))

        # Test login with incorrect credentials
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "wrong"}
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), "There Was An Error Logging In, Try Again..."
        )
