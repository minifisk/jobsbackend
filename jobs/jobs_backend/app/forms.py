""" Forms """

# Core Django imports
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model


# Automaticly activate users who click on link to set a new password received by email
# https://stackoverflow.com/questions/68200102/customize-passwordresetconfirmview 
class SetPasswordFormActivateUserAccount(SetPasswordForm):
    
    def save(self, *args, commit=True, **kwargs):
        user = super().save(*args, commit=False, **kwargs)
        user.is_active = True
        if commit:
            user.save()
        return user

# Allow users who haven't yet activated their accounts to ask for password reset via email
# https://stackoverflow.com/questions/62818777/force-django-to-send-reset-password-email-even-if-usable-password-is-not-set-for 
class PasswordResetFormAllowInactiveUser(PasswordResetForm):

    def get_users(self, nfkc_email):

        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """

        active_users = get_user_model()._default_manager.filter(
            nfkc_email__iexact=nfkc_email) # Removed "is_active=True"
        return (u for u in active_users if u.has_usable_password())