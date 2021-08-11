""" Custom services (functions) related to account management  """

# Standard Library imports
import unicodedata

# Core Django imports
from django.db import transaction
from django.forms.models import model_to_dict

# Third party imports
import marshmallow

# App imports
from jobs_backend.app.validators import EmployerAccountCreationValidator, ApplicantAccountCreationValidator
from jobs_backend.app.models import User
from jobs_backend.app.services import communication_service
from jobs_backend.errors import custom_errors
from jobs_backend.utils import token_utils

# Custom method to create an _EMPLOYER_ account
def create_employer_account(sanitized_email, unsafe_password, sanitized_company_name):

    # Validating sanitized input with custom validation-function
    fields_to_validate_dict = {
        "email": sanitized_email,
        "password": unsafe_password,
        "company_name": sanitized_company_name,
    }

    EmployerAccountCreationValidator().load(fields_to_validate_dict)

    # Normalizing to NFC (best for regular text) and NFKC (best for identifiers) format
    nfc_email = unicodedata.normalize("NFC", sanitized_email)
    nfkc_email = unicodedata.normalize("NFKC", sanitized_email)

    nfc_company_name = unicodedata.normalize("NFC", sanitized_company_name)
    nfkc_company_name = unicodedata.normalize("NFKC", sanitized_company_name)

    # Check if user already exist in database
    if User.objects.filter(nfkc_email=nfkc_email).exists():
        raise custom_errors.EmailAddressAlreadyExistsError()

    # Create new employer-user
    user_model = User.objects.create_user(
        nfc_email=nfc_email, 
        nfkc_email=nfkc_email, 
        nfc_company_name=nfc_company_name, 
        nfkc_company_name=nfkc_company_name,
        password = unsafe_password,
        is_employer = True
    )

    # Send activation email to user
    communication_service.send_user_account_activation_email(user_model)

    # Return auth token to be used by front-end
    auth_token = token_utils.manually_generate_auth_token(user_model)

    return ( user_model, auth_token, )

# Custom method to create an _APPLICANT_ account
def create_applicant_account(sanitized_email, unsafe_password):

    # Validating sanitized input with custom validation-function
    fields_to_validate_dict = {
        "email": sanitized_email,
        "password": unsafe_password,
    }

    ApplicantAccountCreationValidator().load(fields_to_validate_dict)

    # Normalizing to NFC (best for regular text) and NFKC (best for identifiers) format
    nfc_email = unicodedata.normalize("NFC", sanitized_email)
    nfkc_email = unicodedata.normalize("NFKC", sanitized_email)

    # Check if user already exist in database
    if User.objects.filter(nfkc_email=nfkc_email).exists():
        raise custom_errors.EmailAddressAlreadyExistsError()

    # Create new applicant-user
    user_model = User.objects.create_user(
        nfc_email=nfc_email, 
        nfkc_email=nfkc_email,
        password = unsafe_password,
        is_employer = False
    )

    # Send activation email to user
    communication_service.send_user_account_activation_email(user_model)

    # Return auth token to be used by front-end
    auth_token = token_utils.manually_generate_auth_token(user_model)

    return ( user_model, auth_token, )
