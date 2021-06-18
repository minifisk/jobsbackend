from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from ...models import User
from django import utils
from django.conf import settings
from django.urls import reverse


class Command(BaseCommand):
    help = "Generating token for password reset"

    def handle(self, *args, **options):
        try:
            user = User.objects.get(email="alexlindgren08@gmail.com")
            token = PasswordResetTokenGenerator().make_token(user)
            base64_encoded_id = utils.http.urlsafe_base64_encode(utils.encoding.force_bytes(user.id))
            reset_url_args = {'uidb64': base64_encoded_id, 'token': token}
            reset_path = reverse('password_reset_confirm', kwargs=reset_url_args)
            reset_url = f'{settings.BASE_URL}{reset_path}'

            print(user)
            print(token)
            print(reset_url)
        except Exception as e:
            print(e)