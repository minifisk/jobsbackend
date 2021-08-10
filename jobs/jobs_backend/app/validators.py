""" Validators for account creation """

from marshmallow import Schema, fields, validate

from django.conf import settings

# Validator for creating employer accounts, load_only set to True to exclude dump option
# thus, only using the model for API-related tasks and not internal validation
class EmployerAccountCreationValidator(Schema):
    email = fields.Email(required=True, load_only = True, 
        validate=[
        validate.Length(1, 30, error="Email must be between 1 and 30 characters"),
        validate.Regexp("^[a-zA-Z][a-zA-Z0-9@._]*$", error="Email must start with a letter, and "
                            "contain only letters, numbers, dots, @ and underscores. ",),
        ]
    )
    password = fields.Str(required=True, load_only = True, validate=[validate.Length(min=settings.MIN_PASSWORD_LENGTH, error="Password must be at least 8 characters long")],)
    company_name = fields.Str(required=True, load_only = True, validate=[validate.Length(max=20, error="Company name can be max 20 characters")])
    