from django.urls import path
from . import views

urlpatterns = [
    path('postings/', views.posting_list),
    path('postings/<int:pk>/', views.posting_detail),
    path('applicants/', views.applicant_list),
    path('applicants/<int:pk>/', views.applicant_detail),
    path('employers/', views.employer_list),
    path('employers/<int:pk>', views.employer_detail),
    path('applications/', views.application_list),
    path('applications/<int:pk>', views.application_detail)
]