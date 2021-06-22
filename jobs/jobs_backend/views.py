from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import User, Posting, Application
from .serializers import UserSerializer, PostingSerializer, ApplicationSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import views as auth_views
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from django.conf import settings
from urllib.parse import urlencode
import sys
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes






# Create your views here.

""" LOGIN VIEW """
class LoginUser(auth_views.LoginView):
    def get(self, request, *args, **kwargs):
        print("Logging in")  
        print(request.GET.get('token'))
        return super(LoginUser, self).get(request, *args, **kwargs)


""" APPLICANTS """
class ApplicantList(generics.ListCreateAPIView):
    queryset = User.objects.filter(is_employer=False)
    serializer_class = UserSerializer

class ApplicantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(is_employer=False)
    serializer_class = UserSerializer

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
class ApplicationList(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def post(self, request):
        print("post request")
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            request_email = serializer.data['email']

            # Check if user is in database
            try: 
                applicant = User.objects.get(email=request_email)
                print("applicant already exist")
            # If user is not in database
            except:
                #Create a new user
                user = User.objects.create_user(email=request_email)
                print("created new applicant")
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                print(uid)
                token = PasswordResetTokenGenerator().make_token(user)

                if request: 
                    hostname = get_current_site(request)
                else:
                    hostname= Site.objects.get_current().domain
                if sys.argv[1] == "runserver":
                    scheme = 'http'
                elif getattr(settings, 'HTTPS_ENABLED', True):
                    scheme = 'https'
                else:
                    scheme = 'http'
                print(f'{scheme}://{hostname}/reset/{uid}/{token}')



                # Generate token
                
                # Send user an email to the user with the account credentials and a link

                #When user clicks the link 
                            #Force password reset when user clicks the link
                            #Log in user and set_active to true 

   

                
        queryset = self.get_queryset()
        serializer = ApplicationSerializer(queryset, many=True)
        return Response(serializer.data)

class ApplicationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer