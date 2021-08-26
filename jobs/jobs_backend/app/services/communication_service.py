# Standard Library imports
import logging

# Core Django imports
from django import template
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import BadHeaderError, EmailMultiAlternatives


# Third-party imports

# App imports


def send_user_account_activation_email(applicant):

    # Preparing for sending link for password reset for new user
    # Inspiration: https://www.ordinarycoders.com/blog/article/html-password-reset-email-template
    # Inspiration: https://learndjango.com/tutorials/django-password-reset-tutorial

    # Set up data for sending activation email
    subject = "Password Reset Requested"
    plaintext = template.loader.get_template("main/password/password_reset_email.txt")
    htmltemp = template.loader.get_template("main/password/password_reset_email.html")
    c = {
        "email": applicant.nfkc_email,
        "domain": "127.0.0.1:8000",
        "site_name": "Jobs",
        "uid": urlsafe_base64_encode(force_bytes(applicant.pk)),
        "user": applicant,
        "token": PasswordResetTokenGenerator().make_token(applicant),
        "protocol": "http",
    }
    text_content = plaintext.render(c)
    html_content = htmltemp.render(c)

    # Sending email
    try:
        msg = EmailMultiAlternatives(
            subject,
            text_content,
            "Website <admin@example.com>",
            [applicant.nfkc_email],
            headers={"Reply-To": "admin@example.com"},
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        logging.info(
            "From communication_service - Successfully sent user activation email"
        )
    except BadHeaderError:
        logging.info("From communication_service - Error sending user acivation email")
        return HttpResponse("Invalid header found.")
