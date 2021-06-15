from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('postings/', views.PostingList.as_view()),
    path('postings/<int:pk>/', views.PostingDetail.as_view()),
    path('applicants/', views.ApplicantList.as_view()),
    path('applicants/<int:pk>/', views.ApplicantDetail.as_view()),
    path('employers/', views.EmployerList.as_view()),
    path('employers/<int:pk>', views.EmployerDetail.as_view()),
    path('applications/', views.ApplicationList.as_view()),
    path('applications/<int:pk>', views.ApplicationDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)