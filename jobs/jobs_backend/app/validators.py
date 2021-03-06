""" Validators for account creation """
# Python imports
import logging
import pprint

# Core Django imports
from django.conf import settings

# Third part imports
from marshmallow import Schema, fields, validate, validates_schema, ValidationError

# App imports
from ..models import Posting, User, Application

# Logging level
logging.basicConfig(level=logging.INFO)

## REGISTRATION
# "load_only" is set to True to exclude dump option thus, only using the model
# for API-related tasks and not internal validation

# Validator for creating employer accounts,
class EmployerAccountCreationValidator(Schema):
    email = fields.Email(
        required=True,
        load_only=True,
    )
    password = fields.Str(
        required=True,
        load_only=True,
        validate=[
            validate.Length(
                min=settings.MIN_PASSWORD_LENGTH,
                error="Password must be at least 8 characters long",
            )
        ],
    )
    company_name = fields.Str(
        required=True,
        load_only=True,
        validate=[
            validate.Length(max=20, error="Company name can be max 20 characters")
        ],
    )
    is_employer = fields.Boolean(validate=validate.Equal(True))


# Validator for creating applicant accounts
class ApplicantAccountCreationValidator(Schema):
    email = fields.Email(
        required=True,
        load_only=True,
    )
    password = fields.Str(
        required=True,
        load_only=True,
        validate=[
            validate.Length(
                min=settings.MIN_PASSWORD_LENGTH,
                error="Password must be at least 8 characters long",
            )
        ],
    )
    is_employer = fields.Boolean(validate=validate.Equal(False))


## BROWSABLE API SERIALIZERS


class UserSerializer(Schema):
    nfc_email = fields.Email()
    nfkc_email = fields.Email()

    nfc_company_name = fields.String()
    nfkc_company_name = fields.String()

    is_active = fields.Boolean()
    is_employer = fields.Boolean()


class PostingSerializer(Schema):
    employer = fields.Nested(UserSerializer)
    title = fields.String()
    work_title = fields.String()
    description = fields.String()
    work_type = fields.String()
    weekly_hours = fields.Integer()
    locally_bound = fields.Boolean()
    city = fields.String()
    create_at = fields.DateTime()


class ApplicationSerializer(Schema):
    applicant = fields.Nested(UserSerializer)
    posting = fields.Nested(PostingSerializer)
    email = fields.Email()
    cover_letter = fields.String()
    cv_link = fields.Url()
    created_at = fields.DateTime()


## APPLICATION SUBMITTING VALIDATORS


class NewApplicationValidator(Schema):
    posting_id = fields.String()
    email = fields.Email()
    cover_letter = fields.String()
    cv_link = fields.Url()

    # Check so the current user haven't applied to this posting already
    @validates_schema
    def validate_unique_application(self, data, **kwargs):

        # Get current user
        applicant = User.objects.filter(nfkc_email=data["email"])

        # Get posting
        posting = Posting.objects.filter(pk=data["posting_id"])

        if applicant and posting:
            # Get any applications for this user and this posting
            application = Application.objects.filter(
                applicant=applicant[0], posting=posting[0]
            )

            # If any application found for this posting with this user raise Validationerror
            if application:
                raise ValidationError(
                    "An application for this posting has already been made by this user!"
                )

        # If no application was found just log succeeded validation
        logging.info(
            "From validators.py: Ok to create new application, no previous application found"
        )
