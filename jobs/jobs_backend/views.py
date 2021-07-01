""" IMPORTS """

# Fundamental imports
from django.shortcuts import render, redirect

from rest_framework import generics
from rest_framework.response import Response
from .models import User, Posting, Application
from .serializers import UserSerializer, PostingSerializer, ApplicationSerializer
from django.contrib.auth import views as auth_views
import sys
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.template.loader import render_to_string
from django import template
from django.http import JsonResponse
import os
import boto3
import boto3.session
import json
import logging
from django.db.models import Q
from django.contrib.auth.forms import SetPasswordForm
from rest_framework import serializers





# Loggin level
logging.basicConfig(level=logging.INFO)



# Create your views here.

""" LOGIN VIEW """
class LoginUser(auth_views.LoginView):
    def get(self, request, *args, **kwargs):
        return super(LoginUser, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return resolve_url('accounts:login')


""" APPLICANTS """
class ApplicantList(generics.ListCreateAPIView):
    queryset = User.objects.filter(is_employer=False)
    serializer_class = UserSerializer

class ApplicantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(is_employer=False)
    serializer_class = UserSerializer

def Register(request, type):

    if request.method == 'GET':
        if type == "employer":
            return render(request, 'registration/register_employer.html')
        if type == "applicant":
            return render(request, 'registration/register_applicant.html')
    if request.method == 'POST':
        if type == "employer":
            email = request.POST.get('email')
            company_name = request.POST.get('company_name')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password != confirm_password:
                raise serializers.ValidationError("Passwords don't match!")

            context = {'email': email, 'company_name': company_name, 'is_employer': True, 'is_active': True}
    
            serializer = UserSerializer(data=context)

            if serializer.is_valid():
                user = User.objects.create_user(email=email, password=password, is_employer=True, is_active=True)
                logging.info("Created new Employer")

            else:
                logging.info(serializer.errors)
                raise serializers.ValidationError(serializer.errors)

            return render(request, 'registration/register_success.html')

        if type == "applicant":
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password != confirm_password:
                raise serializers.ValidationError("Passwords don't match!")

            context = {'email': email, 'is_employer': False, 'is_active': True, 'company_name': ""}
    
            serializer = UserSerializer(data=context)

            if serializer.is_valid():
                user = User.objects.create_user(email=email, password=password, is_employer=False, is_active=True)
                logging.info("Created new Applicant")

            else:
                logging.info(serializer.errors)
                raise serializers.ValidationError(serializer.errors)

            return render(request, 'registration/register_success.html')


""" EMPLOYERS """
class EmployerList(generics.ListCreateAPIView):
    queryset = User.objects.filter(is_employer=True)
    serializer_class = UserSerializer

class EmployerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(is_employer=True)
    serializer_class = UserSerializer

""" POSTINGS """
class PostingList(generics.ListCreateAPIView):
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer

class PostingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer


""" APPLICATIONS """

def SubmitApplication(request, requested_posting_id):
    requested_posting_id = int(requested_posting_id)
    postings = Posting.objects.all()
    return render(request, 'main/application/application.html', {'postings':postings, 'requested_posting_id': requested_posting_id })

def Sign_s3(request):

    S3_BUCKET = os.environ.get("BUCKET_NAME")

    if (request.method == "GET"):
        file_name = request.GET.get('file_name')
        file_type = request.GET.get('file_type')
        
        s3 = boto3.client('s3', config = boto3.session.Config(signature_version = 's3v4'))
        
        presigned_post = s3.generate_presigned_post(
        Bucket = S3_BUCKET,
        Key = file_name,
        Fields = {"acl": "public-read", "Content-Type": file_type},
        Conditions = [
        {"acl": "public-read"},
        {"Content-Type": file_type}
        ],
        ExpiresIn = 3600
    )

    return JsonResponse({
        "data": presigned_post,
        "url": "https://%s.s3.amazonaws.com/%s" % (S3_BUCKET, file_name)
    })


class ApplicationList(generics.ListCreateAPIView):
    
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    # Inspiration: https://devcenter.heroku.com/articles/s3-upload-python
    def post(self, request):

        posting_id = request.POST.get("postings")
        email = request.POST.get("email")
        cover_letter = request.POST.get("cover_letter")
        cv_link = request.POST.get("cv-url")

        context = {'posting': posting_id, 'email': email, 'cover_letter': cover_letter, 'cv_link': cv_link}
    
        serializer = ApplicationSerializer(data=context)

        # Check if data is valid, for example that no previous application exist
        if serializer.is_valid():
            request_email = serializer.data['email']

            # Check if user is in database
            try: 
                applicant = User.objects.get(email=request_email)
                logging.info("User already in database")
                # Check if user already applied to this posting
             
                # Add a new application to the posting 
                posting = Posting.objects.get(id=posting_id)
                new_application = Application.objects.create(applicant=applicant, posting=posting, email=email, cover_letter=cover_letter,cv_link=cv_link)
                logging.info("Created new application")
            # If user is not in database
            except:
                # Create a new user and storet it in "user"
                applicant = User.objects.create_user(email=request_email)
                logging.info("created new applicant")

                # Add a new application to the posting with the new user
                posting = Posting.objects.get(id=posting_id)
                new_application = Application.objects.create(applicant=applicant, posting=posting, email=email, cover_letter=cover_letter,cv_link=cv_link)
                logging.info("Created new application")

                # Preparing for sending link for password reset for new user
                # Inspiration: https://www.ordinarycoders.com/blog/article/html-password-reset-email-template
                # Inspiration: https://learndjango.com/tutorials/django-password-reset-tutorial
                subject = "Password Reset Requested"
                plaintext = template.loader.get_template('main/password/password_reset_email.txt')
                htmltemp = template.loader.get_template('main/password/password_reset_email.html')
                c = {
                "email":applicant.email,
                'domain':'127.0.0.1:8000',
                'site_name': 'Jobs',
                "uid": urlsafe_base64_encode(force_bytes(applicant.pk)),
                "user": applicant,
                'token': PasswordResetTokenGenerator().make_token(applicant),
                'protocol': 'http',
                }
                text_content = plaintext.render(c)
                html_content = htmltemp.render(c)
                try:
                    logging.info("Sending sign-up email with password reset")
                    msg = EmailMultiAlternatives(subject, text_content, 'Website <admin@example.com>', [applicant.email], headers = {'Reply-To': 'admin@example.com'})
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')

        # If added application is not valid
        else:
            postings = Posting.objects.all()
            messages = serializer.errors
            was_submitted = False
            was_already_submitted = False
            error_message = ""
            print(messages)
            # If applicant already applied to the posting
            if "non_field_errors" in messages:
                if "unique" in messages['non_field_errors'][0]:
                    was_already_submitted = True
                    error_message = messages['non_field_errors'][0]
            else:
                error_message = messages
            # Return template with embedded error messages
            return render(request, 'main/application/application.html', 
            {'postings':postings, 'was_submitted': was_submitted, 
            'was_already_submitted': was_already_submitted, 
            'error_message':error_message})       
        
        # If application was created successfully
        postings = Posting.objects.all()
        was_submitted = True
        was_already_submitted = False
        error_message = ""
        return render(request, 'main/application/application.html', 
        {'postings':postings, 'was_submitted': was_submitted, 
        'was_already_submitted': was_already_submitted, 
        'error_message': error_message}) 

class ApplicationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

""" SEARCH """
def SearchView(request):
    return render(request, 'main/search/search.html')

def SearchQuery(request):

    search = request.GET.get("search")
    queryset = Posting.objects.all()
    payload = []
    if search:
        queryset = queryset.filter(Q(title__icontains=search) | Q(work_title__icontains=search))
        for result in queryset:
            payload.append(result.title + " || " + result.work_title + " || " + "id: " + str(result.id))
    
    return JsonResponse({'status': 200, 'data': payload})

""" PASSWORD RESET """
class MySetPasswordForm(SetPasswordForm):
    
    def save(self, *args, commit=True, **kwargs):
        user = super().save(*args, commit=False, **kwargs)
        user.is_active = True
        if commit:
            user.save()
        return user

""" PROFILE """
def ProfileView(request, pk):

    user_pk = request.user.pk
    browser_pk = pk
    user = User.objects.get(pk=user_pk)

    
    if request.user.is_authenticated == False:
        return redirect('/login')
    else:
        if user_pk != browser_pk:
            return redirect('/profile/' + str(user_pk))
        else:
            applications = Application.objects.filter(applicant=user)
            return render(request, 'main/profile/profile.html', {'applications': applications})