from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from backend.models import Event
import json
from dateutil import parser


class Command(BaseCommand):
    help = "Import events from a JSON file"

    def add_arguments(self, parser):
        parser.add_argument(
            "json_file", type=str, help="Path to the JSON file containing event data"
        )

    def handle(self, *args, **options):
        json_file_path = options["json_file"]
        with open(json_file_path, "r", encoding="utf-8") as file:
            events_data = json.load(file)
            for event_data in events_data:
                try:
                    # Check if close_date is neither None nor an empty string
                    close_date = None
                    if event_data["close_date"] and event_data["close_date"].strip():
                        close_date = parser.parse(event_data["close_date"]).date()

                    # Check if avg_rating is blank or not provided and set it to None if true
                    avg_rating = None
                    if "avg_rating" in event_data and event_data["avg_rating"] not in (
                        None,
                        "",
                        " ",
                    ):
                        avg_rating = event_data["avg_rating"]

                    location = (
                        event_data["location"] if "location" in event_data else ""
                    )

                    description = (
                        event_data["description"] if "description" in event_data else ""
                    )

                    external_links = event_data.get("external_links", [])

                    event = Event.objects.create(
                        title=event_data["title"],
                        category=event_data["category"],
                        description=description,
                        open_date=parser.parse(event_data["open_date"]).date(),
                        close_date=close_date,
                        location=location,
                        external_links=external_links,
                        image_url=event_data["image_url"],
                        avg_rating=avg_rating,
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Successfully imported event: {event.title}"
                        )
                    )
                except ValidationError as e:
                    self.stdout.write(self.style.ERROR(f"Error importing event: {e}"))
