from django.contrib import admin
from .models import Applicant, Employer, Posting, Application

# Register your models here.

class ApplicantAdmin(admin.ModelAdmin):
    fields = ['email', 'first_name', 'last_name']

admin.site.register(Applicant, ApplicantAdmin)

class EmployerAdmin(admin.ModelAdmin):
    fields = ['email', 'company_name']

admin.site.register(Employer, EmployerAdmin)

class PostingAdmin(admin.ModelAdmin):
    fields = ['employer', 'title', 'work_title', 'description', 'work_type', 'weekly_hours', 'locally_bound', 'city']

admin.site.register(Posting, PostingAdmin)

class ApplicationAdmin(admin.ModelAdmin):
    fields = ['applicant', 'posting', 'cover_letter', 'cv_link']

admin.site.register(Application, ApplicationAdmin)


