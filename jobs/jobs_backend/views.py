from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Applicant, Employer, Posting, Application
from .serializers import ApplicantSerializer, EmployerSerializer, PostingSerializer, ApplicationSerializer

# Create your views here.

""" APPLICANTS """
@csrf_exempt
def applicant_list(request):
    """
    List all applicants, or create new applicant
    """
    if request.method == 'GET':
        applicants = Applicant.objects.all()
        serializer = ApplicantSerializer(applicants, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ApplicantSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def applicant_detail(request, pk):
    """
    Retrieve, update or delete an applicant
    """
    try:
        applicant = Applicant.objects.get(pk=pk)
    except Applicant.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = ApplicantSerializer(applicant)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PostingSerializer(applicant, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        applicant.delete()
        return HttpResponse(status=204)

""" EMPLOYERS """
@csrf_exempt
def employer_list(request):
    """
    List all employers, or create new employer
    """
    if request.method == 'GET':
        employers = Employer.objects.all()
        serializer = EmployerSerializer(employers, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = EmployerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def employer_detail(request, pk):
    """
    Retrieve, update or delete an employer
    """
    try:
        employer = Employer.objects.get(pk=pk)
    except Employer.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = EmployerSerializer(employer)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = EmployerSerializer(employer, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        employer.delete()
        return HttpResponse(status=204)


""" POSTINGS """
@csrf_exempt
def posting_list(request):
    """
    List all postings, or create new posting
    """
    if request.method == 'GET':
        postings = Posting.objects.all()
        serializer = PostingSerializer(postings, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PostingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def posting_detail(request, pk):
    """
    Retrieve, update or delete a posting
    """
    try:
        posting = Posting.objects.get(pk=pk)
    except Posting.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = PostingSerializer(posting)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PostingSerializer(posting, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        posting.delete()
        return HttpResponse(status=204)


""" APPLICATIONS """
@csrf_exempt
def application_list(request):
    """
    List all applications, or create new application
    """
    if request.method == 'GET':
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ApplicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def application_detail(request, pk):
    """
    Retrieve, update or delete an application
    """
    try:
        application = Application.objects.get(pk=pk)
    except Application.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = ApplicationSerializer(application)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ApplicationSerializer(application, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        application.delete()
        return HttpResponse(status=204)