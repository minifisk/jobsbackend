
# Django core imports

# Third-party imports
from django.db.models import query
from rest_framework import generics

# App imports
from jobs_backend.app.models import User, Posting, Application
from jobs_backend.app.serializers import UserSerializer, PostingSerializer, ApplicationSerializer
from jobs_backend.app.validators import PostingSerializer as NewPostingSerializer

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
    serializer_class = NewPostingSerializer

class PostingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer
