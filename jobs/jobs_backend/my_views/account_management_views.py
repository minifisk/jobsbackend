# Disabling pylint for unused variable when creating new user:
# pylint: disable=unused-variable

""" Views for managing user accounts """

# Core Django imports
import logging
from django.shortcuts import render, resolve_url

# Third-party imports
from django.contrib.auth import views as auth_views
from rest_framework import serializers

# App imports
from ..models import User
from ..serializers import UserSerializer

# Loggin level
logging.basicConfig(level=logging.INFO)


class LoginUser(auth_views.LoginView):
    """View for logging in user"""

    def get_success_url(self):
        return resolve_url("accounts:login")


def user_view(request, account_type):
    """View for handling user registration"""

    # Generating different templates depending on type of
    # account_type being registred (given as a query parameter)
    if request.method == "GET":
        if account_type == "employer":
            return render(request, "registration/register_employer.html")
        if account_type == "applicant":
            return render(request, "registration/register_applicant.html")

    if request.method == "POST":
        if account_type == "employer":
            email = request.POST.get("email")
            company_name = request.POST.get("company_name")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            if password != confirm_password:
                raise serializers.ValidationError("Passwords don't match!")

            context = {
                "email": email,
                "company_name": company_name,
                "is_employer": True,
                "is_active": True,
            }

            serializer = UserSerializer(data=context)

            if serializer.is_valid():
                user = User.objects.create_user(
                    email=email, password=password, is_employer=True, is_active=True
                )
                logging.info("Created new Employer")

            else:
                logging.info(serializer.errors)
                raise serializers.ValidationError(serializer.errors)

            return render(request, "registration/register_success.html")

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
