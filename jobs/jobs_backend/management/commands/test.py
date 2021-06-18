from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Testing"

    def handle(self, *args, **options):
        try:
            print("Hello")
        except:
            raise CommandError("Something went wrong")