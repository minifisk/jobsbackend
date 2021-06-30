from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

# Inspiration for password reset views taken from: https://www.ordinarycoders.com/blog/article/django-password-reset#comments
urlpatterns = [
    path('', views.SearchView, name="home"),
    path('accounts/',include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="main/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='main/password/password_reset_complete.html'), name='password_reset_complete'),
    path('postings/', views.PostingList.as_view()),
    path('postings/<int:pk>/', views.PostingDetail.as_view()),
    path('applicants/', views.ApplicantList.as_view()),
    path('applicants/<int:pk>/', views.ApplicantDetail.as_view()),
    path('employers/', views.EmployerList.as_view()),
    path('employers/<int:pk>', views.EmployerDetail.as_view()),
    path('applications/', views.ApplicationList.as_view()),
    path('applications/<int:pk>', views.ApplicationDetail.as_view()),
    path('submitapplication/<requested_posting_id>', views.SubmitApplication, name="submit_application"),
    path('sign_s3/', views.Sign_s3, name="sign_s3"),
    path('search/', views.SearchQuery, name="search_query")

]

urlpatterns = format_suffix_patterns(urlpatterns)