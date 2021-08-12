""" Validators for account creation """

from marshmallow import Schema, fields, validate

from django.conf import settings

# "load_only" is set to True to exclude dump option thus, only using the model 
# for API-related tasks and not internal validation

# Validator for creating employer accounts, 
class EmployerAccountCreationValidator(Schema):
    email = fields.Email(required=True, load_only = True,)
    password = fields.Str(required=True, load_only = True, validate=[validate.Length(min=settings.MIN_PASSWORD_LENGTH, error="Password must be at least 8 characters long")],)
    company_name = fields.Str(required=True, load_only = True, validate=[validate.Length(max=20, error="Company name can be max 20 characters")])
    is_employer = fields.Boolean(validate=validate.Equal(True))
    
# Validator for creating applicant accounts
class ApplicantAccountCreationValidator(Schema):
    email = fields.Email(required=True, load_only = True,)
    password = fields.Str(required=True, load_only = True, validate=[validate.Length(min=settings.MIN_PASSWORD_LENGTH, error="Password must be at least 8 characters long")],)
    is_employer = fields.Boolean(validate=validate.Equal(False))