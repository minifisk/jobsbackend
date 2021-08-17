""" Views for submitting an application to a job posting   """

# Python packages imports
import os

# Django core imports
from django.shortcuts import render
from django.http import JsonResponse


# Third-party imports
import boto3

# App imports
from jobs_backend.app.models import User, Application, Posting


# View for generating a template with a submit-form for a job posting
def SubmitApplicationView(request, requested_posting_id):
    
    # Get the ID for the requested posting in the query
    requested_posting_id = int(requested_posting_id)

    # Get all list of all postings
    postings = Posting.objects.all()

    # Return a template with the requested posting ID and an object with all postings
    return render(request, 'main/submit_application/submit_application.html', {'postings':postings, 'requested_posting_id': requested_posting_id })


# View for generating a signed URL to AWS bucket to be used for uploading a users CV
# used in the templates/main/submit_application-template
def Sign_s3(request):

    # Getting the name of the bucket from environment variable
    S3_BUCKET = os.environ.get("BUCKET_NAME")

    # Only allowing GET requests
    if (request.method == "GET"):

        # Getting the randomly generated UUID file-name from the JS in the template
        file_name = request.GET.get('file_name')

        # Limiting file-uploads to be in PDF format
        file_type = "application/pdf"
        
        # Setting up a boto3 client with signature-version s3V4
        s3 = boto3.client('s3', config = boto3.session.Config(signature_version = 's3v4'))
        
        # Generating a presigned post
        presigned_post = s3.generate_presigned_post(
        Bucket = S3_BUCKET,
        Key = file_name,
        Fields = {"acl": "public-read", "Content-Type": file_type},
        Conditions = [
        {"acl": "public-read"},
        {"Content-Type": file_type},
        ["Content-length-range", 10000, 10000000] # Allowing uploads from 10 kb to 10 mb
        ],
        ExpiresIn = 3600
    )

    return JsonResponse({
        "data": presigned_post,
        "url": "https://%s.s3.amazonaws.com/%s" % (S3_BUCKET, file_name)
    })