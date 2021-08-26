# Disabling pylint for unused variable when creating new user:
# pylint: disable=unused-variable

""" Views for managing user accounts """

# Core Django imports
import logging
from django import http
from django.shortcuts import render, resolve_url

# Third-party imports
from django.contrib.auth import views as auth_views
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
import marshmallow

# App imports
from jobs_backend.utils import sanitization_utils
from jobs_backend.app.services import account_management_services
from jobs_backend.utils.error_utils import (
    get_validation_error_response,
    get_business_requirement_error_response,
)
from jobs_backend.errors import custom_errors
from django.contrib.auth.forms import SetPasswordForm

# Logging level
logging.basicConfig(level=logging.INFO)


# View used when user request a password reset
class MySetPasswordForm(SetPasswordForm):
    def save(self, *args, commit=True, **kwargs):
        user = super().save(*args, commit=False, **kwargs)
        user.is_active = True  # Setting is_active to True to enable email confirmation
        if commit:
            user.save()
        return user


class User(APIView):

    # Generating different templates depending on type of account_type being registred
    def get(self, request, account_type):
        if account_type == "employer":
            return render(request, "registration/register_employer.html")
        if account_type == "applicant":
            return render(request, "registration/register_applicant.html")

    # Registrating accounts
    def post(self, request, account_type):

        # Registrating an employer account
        if account_type == "employer":

            # Getting data from the request
            unsafe_email = request.POST.get("email")
            unsafe_company_name = request.POST.get("company_name")
            unsafe_password = request.POST.get("password")
            unsafe_confirm_password = request.POST.get("confirm_password")
            is_employer = True

            # Check password confirmation
            if unsafe_password != unsafe_confirm_password:
                raise serializers.ValidationError("Passwords don't match!")

            # Sanitizing imput
            sanitized_email = sanitization_utils.strip_xss(unsafe_email)
            sanitized_company_name = sanitization_utils.strip_xss(unsafe_company_name)

            # Trying registration of account and logging completion
            try:
                (
                    user_model,
                    auth_token,
                ) = account_management_services.create_employer_account(
                    sanitized_email,
                    unsafe_password,
                    sanitized_company_name,
                    is_employer,
                )
                logging.info("Created new Employer account")

            # Validation error & custom errors
            except marshmallow.exceptions.ValidationError as e:
                return get_validation_error_response(
                    validation_error=e, http_status_code=422
                )
            except custom_errors.EmailAddressAlreadyExistsError as e:
                return get_business_requirement_error_response(
                    business_logic_error=e, http_status_code=409
                )

            # Return the auth token recieved on registration for front-end use
            resp = {"data": {"auth_token": auth_token}}
            return Response(data=resp, status=201)

        # Registrating an applicant-account
        if account_type == "applicant":

            # Getting data from the request
            unsafe_email = request.POST.get("email")
            unsafe_password = request.POST.get("password")
            unsafe_confirm_password = request.POST.get("confirm_password")
            is_employer = False

            # Check password confirmation
            if unsafe_password != unsafe_confirm_password:
                raise serializers.ValidationError("Passwords don't match!")

            # Sanitizing imput
            sanitized_email = sanitization_utils.strip_xss(unsafe_email)

            # Trying registration of account and logging completion
            try:
                (
                    user_model,
                    auth_token,
                ) = account_management_services.create_applicant_account(
                    sanitized_email, unsafe_password, is_employer
                )
                logging.info("Created new Applicant account")

            # Validation error & custom errors
            except marshmallow.exceptions.ValidationError as e:
                return get_validation_error_response(
                    validation_error=e, http_status_code=422
                )
            except custom_errors.EmailAddressAlreadyExistsError as e:
                return get_business_requirement_error_response(
                    business_logic_error=e, http_status_code=409
                )

            # Return the auth token recieved on registration for front-end use
            resp = {"data": {"auth_token": auth_token}}
            return Response(data=resp, status=201)
