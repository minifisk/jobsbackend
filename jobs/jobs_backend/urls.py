# Inspiration for password reset views taken from:
# https://www.ordinarycoders.com/blog/article/django-password-reset#comments

""" URLs for jobs_backend """

# Core Django Imports
from django.urls import path, include
from django.contrib.auth import views as auth_views

# Third party imports
from rest_framework.urlpatterns import format_suffix_patterns

# App imports
from jobs_backend.my_views import account_management_views
from . import views


urlpatterns = [
    # INDEX ROUTE
    path("", views.SearchView, name="home"),
    # ACCOUNT MANAGEMENT ROUTES
    ## Default accounts route,
    path("accounts/", include("django.contrib.auth.urls")),
    ## Custom register route for employers/applicants
    path("register/<str:type>", account_management_views.user_view, name="register"),
    ## Custom login route to /login instead of /accounts/login
    path("login/", auth_views.LoginView.as_view(), name="login"),
    ## Custom reset route for using custom template
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="main/password/password_reset_confirm.html",
            form_class=views.MySetPasswordForm,
        ),
        name="password_reset_confirm",
    ),
    ## Custom reset confirm route for using custom template
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="main/password/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # INTERNALLY USED ENDPOINTS
    ## Endpoint for generating a signed URL for users uploaded CV
    path("sign_s3/", views.Sign_s3, name="sign_s3"),
    ## Endpoint for generating search results on index page
    path("search/", views.SearchQuery, name="search_query"),
    # USER RELEVANT ENDPOINTS
    ## Profile endpoint for seeing current applications
    path("profile/<int:pk>", views.ProfileView, name="profile_view"),
    ## Endpoint for generating a submit template for a certain posting
    path(
        "submitapplication/<requested_posting_id>",
        views.SubmitApplication,
        name="submit_application",
    ),
    # "INSPECT" ENDPOINTS FOR DEVELOPERS
    ## Postings endpoints for seeing one or all postings
    path("postings/", views.PostingList.as_view()),
    path("postings/<int:pk>/", views.PostingDetail.as_view()),
    ## Applicants endpoints for seseing one or all applicants
    path("applicants/", views.ApplicantList.as_view()),
    path("applicants/<int:pk>/", views.ApplicantDetail.as_view()),
    ## Employer endpoint for seing one or all employers
    path("employers/", views.EmployerList.as_view()),
    path("employers/<int:pk>", views.EmployerDetail.as_view()),
    ## Application endpoint for seing one or all applications
    path("applications/", views.ApplicationList.as_view()),
    path("applications/<int:pk>", views.ApplicationDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
