""" Views for submitting an application to a job posting   """

# Python packages imports
from django import http
import os
import json
import logging

# Django core imports
from django.shortcuts import render
from django.http import JsonResponse


# Third-party imports
import boto3
from marshmallow import ValidationError
import marshmallow


# App imports
from jobs_backend.app.models import User, Application, Posting
from jobs_backend.utils import sanitization_utils, error_utils
from jobs_backend.app.validators import NewApplicationValidator
from jobs_backend.app.services import communication_service


# View for generating template for submitting an application to a posting
def SubmitApplicationView(request, requested_posting_id):

    # Convert posting_id to int to be sent with template
    requested_posting_id = int(requested_posting_id)

    # Get all postings to be sent with the template
    postings = Posting.objects.all()

    was_submitted = False
    was_already_submitted = False
    error_message = ""
    return render(
        request,
        "main/submit_application/submit_application.html",
        {
            "postings": postings,
            "was_submitted": was_submitted,
            "was_already_submitted": was_already_submitted,
            "error_message": error_message,
        },
    )


# View for handling submitting applications to job postings
def SubmitApplication(request):

    # Submit the application when getting a POST request
    if request.method == "POST":
        # Inspiration: https://devcenter.heroku.com/articles/s3-upload-python

        # Get relevant data from POST request
        unsafe_posting_id = request.POST.get("postings")
        unsafe_email = request.POST.get("email")
        unsafe_cover_letter = request.POST.get("cover_letter")
        unsafe_cv_link = request.POST.get("cv-url")

        # Sanitize input
        sanitized_posting_id = sanitization_utils.strip_xss(unsafe_posting_id)
        sanitized_email = sanitization_utils.strip_xss(unsafe_email)
        sanitized_cover_letter = sanitization_utils.strip_xss(unsafe_cover_letter)
        sanitized_cv_link = sanitization_utils.strip_xss(unsafe_cv_link)

        # Store data in variable context
        context = {
            "posting_id": sanitized_posting_id,
            "email": sanitized_email,
            "cover_letter": sanitized_cover_letter,
            "cv_link": sanitized_cv_link,
        }

        # Try validating input type and that no application from this user exist for this posting
        try:
            NewApplicationValidator().load(context)

            # Validation succeeded
            logging.info(
                "From submit_application_views - Registration data validated successfully!"
            )

            # Check if a new user account need to be created or using exisitng one
            try:
                # Try finding applicant with inputted email
                applicant = User.objects.get(nfkc_email=sanitized_email)
                logging.info("From submit_application_views - User already in database")

                # If user found, get curent posting
                posting = Posting.objects.get(id=sanitized_posting_id)

                # Create a new application with user and posting
                new_application = Application.objects.create(
                    applicant=applicant,
                    posting=posting,
                    cover_letter=sanitized_cover_letter,
                    cv_link=sanitized_cv_link,
                )
                logging.info(
                    "From submit_application_views - Created new application with existing user account"
                )

            # If no user with email user in creating application exist...
            except:
                # Create a new user
                applicant = User.objects.create_user(nfkc_email=sanitized_email)
                logging.info(
                    "From submit_application_views - No user with email found, created new user"
                )

                # Send user a confirmation email for generating a password to their account
                """ INSERT SEND EMAIL SERVICE HERE """
                communication_service.send_user_account_activation_email(applicant)

                # Add a new application to the posting with the new user
                posting = Posting.objects.get(id=sanitized_posting_id)
                new_application = Application.objects.create(
                    applicant=applicant,
                    posting=posting,
                    cover_letter=sanitized_cover_letter,
                    cv_link=sanitized_cv_link,
                )
                logging.info(
                    "From submit_application_views - Created new application with new user account"
                )

                # Instantiate variables to be used in template
                postings = Posting.objects.all()
                was_submitted = True
                was_already_submitted = False

                # Generate template with message that application was submitted
                logging.info("Generating template with success message")
                return render(
                    request,
                    "main/submit_application/submit_application.html",
                    {
                        "postings": postings,
                        "was_submitted": was_submitted,
                        "was_already_submitted": was_already_submitted,
                    },
                )

        # If validation returned validation error
        except marshmallow.exceptions.ValidationError as e:
            logging.info(
                "From submit_application_views - Registration data failed to be validated! Error_msg: %s"
                % (e)
            )

            """ If using separate front-end (like React)"""
            # return error_utils.get_validation_error_response(validation_error=e, http_status_code=422)

            """ If using Django templates """
            # Instantiate variables to be used in template
            postings = Posting.objects.all()
            was_submitted = False
            was_already_submitted = False

            # Generate template with embedded error message that posting was already submitted from this user
            logging.info("Generating template with error message")
            return render(
                request,
                "main/submit_application/submit_application.html",
                {
                    "postings": postings,
                    "was_submitted": False,
                    "was_already_submitted": True,
                },
            )


# View for generating a signed URL to AWS bucket to be used for uploading a users CV
# used in the templates/main/submit_application-template
def Sign_s3(request):

    # Getting the name of the bucket from environment variable
    S3_BUCKET = os.environ.get("BUCKET_NAME")

    # Only allowing GET requests
    if request.method == "GET":

        # Getting the randomly generated UUID file-name from the JS in the template
        file_name = request.GET.get("file_name")

        # Limiting file-uploads to be in PDF format
        file_type = "application/pdf"

        # Setting up a boto3 client with signature-version s3V4
        s3 = boto3.client("s3", config=boto3.session.Config(signature_version="s3v4"))

        # Generating a presigned post
        presigned_post = s3.generate_presigned_post(
            Bucket=S3_BUCKET,
            Key=file_name,
            Fields={"acl": "public-read", "Content-Type": file_type},
            Conditions=[
                {"acl": "public-read"},
                {"Content-Type": file_type},
                [
                    "Content-length-range",
                    10000,
                    10000000,
                ],  # Allowing uploads from 10 kb to 10 mb
            ],
            ExpiresIn=3600,
        )

    # Returning the presigned post and url
    return JsonResponse(
        {
            "data": presigned_post,
            "url": "https://%s.s3.amazonaws.com/%s" % (S3_BUCKET, file_name),
        }
    )
