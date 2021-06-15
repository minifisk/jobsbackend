from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .models import Applicant, Employer, Posting, Application
from .serializers import ApplicantSerializer, EmployerSerializer, PostingSerializer, ApplicationSerializer

# Create your views here.

""" APPLICANTS """
@csrf_exempt
@api_view(['GET', 'POST'])
def applicant_list(request, format=None):
    """
    List all applicants, or create new applicant
    """
    if request.method == 'GET':
        applicants = Applicant.objects.all()
        serializer = ApplicantSerializer(applicants, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ApplicantSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def applicant_detail(request, pk, format=None):
    """
    Retrieve, update or delete an applicant
    """
    try:
        applicant = Applicant.objects.get(pk=pk)
    except Applicant.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ApplicantSerializer(applicant)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostingSerializer(applicant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        applicant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

""" EMPLOYERS """
@csrf_exempt
@api_view(['GET', 'POST'])
def employer_list(request, format=None):
    """
    List all employers, or create new employer
    """
    if request.method == 'GET':
        employers = Employer.objects.all()
        serializer = EmployerSerializer(employers, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = EmployerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def employer_detail(request, pk, format=None):
    """
    Retrieve, update or delete an employer
    """
    try:
        employer = Employer.objects.get(pk=pk)
    except Employer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = EmployerSerializer(employer)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EmployerSerializer(applicant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        employer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


""" POSTINGS """
@csrf_exempt
@api_view(['GET', 'POST'])
def posting_list(request, format=None):
    """
    List all postings, or create new posting
    """
    if request.method == 'GET':
        postings = Posting.objects.all()
        serializer = PostingSerializer(postings, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PostingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def posting_detail(request, pk, format=None):
    """
    Retrieve, update or delete a posting
    """
    try:
        posting = Posting.objects.get(pk=pk)
    except Posting.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PostingSerializer(posting)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostingSerializer(applicant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        posting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


""" APPLICATIONS """
@csrf_exempt
@api_view(['GET', 'POST'])
def application_list(request, format=None):
    """
    List all applications, or create new application
    """
    if request.method == 'GET':
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ApplicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def application_detail(request, pk, format=None):
    """
    Retrieve, update or delete an application
    """
    try:
        application = Application.objects.get(pk=pk)
    except Application.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ApplicationSerializer(application)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ApplicationSerializer(application, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)