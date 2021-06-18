from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    
    """ User model """
    username = None
    first_name = None
    last_name = None

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    company_name = models.CharField(max_length=50, blank=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return '%s %s' % (self.email, self.company_name)

class Posting(models.Model):
    FULLTIME = "FT"
    PARTTIME = "PT"
    TEMPORARY = "TP"
    CONSULTANT = "CT"
    WORK_TYPE_CHOICES = [
        (FULLTIME, "Fulltime"),
        (PARTTIME, "Parttime"), 
        (TEMPORARY, "Temporary"),
        (CONSULTANT, "Consultant")
    ]

    employer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="related employer", blank=False)
    title = models.CharField(max_length=150, blank=False)
    work_title = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=500, blank=False)
    work_type = models.CharField(max_length=2, choices=WORK_TYPE_CHOICES, default=FULLTIME)
    weekly_hours = models.IntegerField(blank=False)
    locally_bound = models.BooleanField(blank=False, default=True)
    city = models.CharField(max_length=30, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.title, self.city)

class Application(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="related applicant", blank=True, null=True)
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE, verbose_name="related posting", blank=False)
    email = models.EmailField(blank=False, unique=True)
    cover_letter = models.CharField(max_length=3000, blank=False)
    cv_link = models.URLField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email





