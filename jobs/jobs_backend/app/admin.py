from django.contrib import admin
from .models import User, Posting, Application

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    model = User
    fields = ['email']

admin.site.register(User, CustomUserAdmin)

class PostingAdmin(admin.ModelAdmin):
    fields = ['employer', 'title', 'work_title', 'description', 'work_type', 'weekly_hours', 'locally_bound', 'city']

admin.site.register(Posting, PostingAdmin)

class ApplicationAdmin(admin.ModelAdmin):
    fields = ['applicant', 'posting', 'cover_letter', 'cv_link']

admin.site.register(Application, ApplicationAdmin)


