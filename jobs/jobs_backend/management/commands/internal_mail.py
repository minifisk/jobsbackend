

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail


class Command(BaseCommand):
    help = "Testing email"

    def handle(self, *args, **options):
        try:
            send_mail(
            'Subject here',
            'Here is the message.',
            'from@example.com',
            ['to@example.com'],
            fail_silently=False,
            )
        except:
            raise CommandError("Something went wrong")