# Inspiration for password reset views taken from:
# https://www.ordinarycoders.com/blog/article/django-password-reset#comments

""" URLs for jobs_backend """

import pdb

# Core Django Imports
from django.urls import path, include
from django.contrib.auth import views as auth_views

# Third party imports
from rest_framework.urlpatterns import format_suffix_patterns

# App imports
from jobs_backend.app.forms import (
    PasswordResetFormAllowInactiveUser,
    SetPasswordFormActivateUserAccount,
)
from jobs_backend.app.views import account_management_views
from jobs_backend.app.views import browsable_api_views
from jobs_backend.app.views import search_views
from jobs_backend.app.views import user_views
from jobs_backend.app.views import submit_application_views
from . import views

urlpatterns = [
    ##############
    # SEARCH VIEWS
    ##############
    path("", search_views.SearchView, name="home"),
    ## Endpoint for generating search results on index page
    path("search/", search_views.SearchQuery, name="search_query"),
    ###############################
    # DJANGO DEFAULT ACCOUNT ROUTES
    ###############################
    ## Default accounts route,
    path("accounts/", include("django.contrib.auth.urls")),
    ##################
    ## REGISTER ROUTES
    ##################
    ## Custom register route for employers/applicants
    ## for: sers who are creating a new account
    path(
        "register/<str:account_type>",
        account_management_views.User.as_view(),
        name="register",
    ),
    ## Custom login route to /login instead of /accounts/login
    ## for: users who are logging in
    path("login/", auth_views.LoginView.as_view(), name="login"),
    #######################
    # PASSWORD RESET ROUTES
    #######################
    ## Password reset view
    ## for: users who click reset link on website
    ## using: custom form allowing also inactive users to reset password
    path(
        "reset/",
        auth_views.PasswordResetView.as_view(
            form_class=PasswordResetFormAllowInactiveUser
        ),
        name="password_reset_complete",
    ),
    ## Password reset view
    ## for: users who have clicked reset password link in email
    ## using: custom form that activate inactive users
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="main/password/password_reset_confirm.html",
            form_class=SetPasswordFormActivateUserAccount,
        ),
        name="password_reset_confirm",
    ),
    ## Password reset confirm route
    ## for: users who have successfully reset their password to a new one
    ## using: custom template
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="main/password/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    ##############################
    # SUBMITTING APPLICATION VIEWS
    ##############################
    ## Endpoint for generating a signed URL on AWS for a users uploaded CV
    path("sign_s3/", submit_application_views.Sign_s3, name="sign_s3"),
    ## Endpoint for generating a submit template for a new job application
    path(
        "submitapplication/<requested_posting_id>",
        submit_application_views.SubmitApplicationView,
        name="submit_application_view",
    ),
    ## Endpoint for handling creation of new applications
    path(
        "submitapplication/",
        submit_application_views.SubmitApplication,
        name="submit_application",
    ),
    ######################
    # BROWSABLE USER VIEWS
    ######################
    ## Profile endpoint for seeing current applications
    path("profile/<int:pk>", user_views.ProfileView, name="profile_view"),
    # "INSPECT" ENDPOINTS FOR DEVELOPERS
    ## Postings endpoints for seeing one or all postings
    path("postings/", browsable_api_views.PostingList.as_view()),
    path("postings/<int:pk>/", browsable_api_views.PostingDetail.as_view()),
    ## Applicants endpoints for seseing one or all applicants
    path("applicants/", browsable_api_views.ApplicantList.as_view()),
    path("applicants/<int:pk>/", browsable_api_views.ApplicantDetail.as_view()),
    ## Employer endpoint for seing one or all employers
    path("employers/", browsable_api_views.EmployerList.as_view()),
    path("employers/<int:pk>", browsable_api_views.EmployerDetail.as_view()),
    ## Application endpoint for seing one or all applications
    path("applications/", browsable_api_views.ApplicationList.as_view()),
    path("applications/<int:pk>", browsable_api_views.ApplicationDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
