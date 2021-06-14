from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField(blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)

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

    title = models.CharField(max_length=150, blank=False)
    work_title = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=500, blank=False)
    work_type = models.CharField(max_length=2, choices=WORK_TYPE_CHOICES, default=FULLTIME)
    weekly_hours = models.IntegerField(blank=False)
    localy_bound = models.BooleanField(blank=False, default=True)
    city = models.CharField(max_length=30, blank=False)

class Application(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE)
    cover_letter = models.CharField(max_length=3000, blank=False)
    cv_link = models.URLField(max_length=500, blank=False)




