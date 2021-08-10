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
from jobs_backend.app.models import User
from jobs_backend.app.serializers import UserSerializer
from jobs_backend.utils import sanitization_utils
from jobs_backend.app.services import account_management_services
from jobs_backend.utils.error_utils import get_validation_error_response, get_business_requirement_error_response
from jobs_backend.errors import custom_errors

# Logging level
logging.basicConfig(level=logging.INFO)


class LoginUser(auth_views.LoginView):
    """View for logging in user"""

    def get_success_url(self):
        return resolve_url("accounts:login")


class User(APIView):

    def get(self, request, account_type):
    # Generating different templates depending on type of
    # account_type being registred (given as a query parameter)
        if account_type == "employer":
            return render(request, "registration/register_employer.html")
        if account_type == "applicant":
            return render(request, "registration/register_applicant.html")

    def post(self, request, account_type):
        if account_type == "employer":
            unsafe_email = request.POST.get("email")
            unsafe_company_name = request.POST.get("company_name")
            unsafe_password = request.POST.get("password")
            unsafe_confirm_password = request.POST.get("confirm_password")

            if unsafe_password != unsafe_confirm_password:
                raise serializers.ValidationError("Passwords don't match!")

            sanitized_email = sanitization_utils.strip_xss(unsafe_email)
            sanitized_company_name = sanitization_utils.strip_xss(unsafe_company_name)

            try:
                user_model, auth_token = account_management_services.create_employer_account(
                    sanitized_email,
                    unsafe_password,
                    sanitized_company_name
                )
                logging.info("Created new Employer")

            except marshmallow.exceptions.ValidationError as e:
                return get_validation_error_response(validation_error=e, http_status_code=422)
            except custom_errors.EmailAddressAlreadyExistsError as e:
                return get_business_requirement_error_response(business_logic_error=e, http_status_code=409)


            resp = { "data": { "auth_token": auth_token } }
            return Response(data=resp, status=201)


        if account_type == "applicant":
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            if password != confirm_password:
                raise serializers.ValidationError("Passwords don't match!")

            context = {"email": email, "is_employer": False, "is_active": True, "company_name": ""}

            serializer = UserSerializer(data=context)

            if serializer.is_valid():
                user = User.objects.create_user(
                    email=email, password=password, is_employer=False, is_active=True
                )
                logging.info("Created new Applicant")

            else:
                logging.info(serializer.errors)
                raise serializers.ValidationError(serializer.errors)

            return render(request, "registration/register_success.html")
        return render(request, "registration/register_fail.html")
