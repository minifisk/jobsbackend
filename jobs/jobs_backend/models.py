from django.db import models

# Create your models here.
class Applicant(models.Model):
    email = models.EmailField(blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

class Employer(models.Model):
    email = models.EmailField(blank=False)
    company_name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return '%s %s' % (self.company_name, self.email)


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

    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, verbose_name="related employer", blank=False)
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
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, verbose_name="related applicant", blank=False)
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE, verbose_name="related posting", blank=False)
    cover_letter = models.CharField(max_length=3000, blank=False)
    cv_link = models.URLField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s %s' % (self.applicant.first_name, self.applicant.last_name, self.posting.title)





