from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager

# Create your models here.


""" CUSTOM USERMANAGER FOR CUSTOM USERMODEL TO ALLOW FOR USERS WITH EMAIL AS USERNAME """
class CustomUserManager(UserManager):

    def _create_user(self, nfkc_email, unsafe_password, **extra_fields):
        nfkc_email = self.normalize_email(nfkc_email)
        user = User(nfkc_email=nfkc_email, **extra_fields)
        user.password = make_password(unsafe_password)
        user.save(using=self._db)
        return user

    def create_user(self, nfkc_email, unsafe_password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(nfkc_email, unsafe_password, **extra_fields)

    def create_superuser(self, nfkc_email, unsafe_password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        assert extra_fields['is_staff']
        assert extra_fields['is_superuser']
        return self._create_user(nfkc_email, unsafe_password, **extra_fields)

""" CUSTOM USER MODEL WITH EMAIL AS USERNAME """
class User(AbstractUser):

    username = None
    first_name = None
    last_name = None
    email = None

    """ Storing both NFC format (display to user on web) 
    and NFKC (searching and guaranteering uniqueness) """
    nfc_email = models.EmailField()
    nfkc_email = models.EmailField(unique=True)

    nfc_company_name = models.CharField(max_length=50, blank=True)
    nfkc_company_name = models.CharField(max_length=50, blank=True) 

    is_active = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)

    USERNAME_FIELD = "nfkc_email" # Set the NFKC email field to the username field
    EMAIL_FIELD = "nfkc_email" # Set the default email field (used in password reset, etc) to NFKC email field
    REQUIRED_FIELDS = [nfkc_email]

    objects = CustomUserManager() 

    def __str__(self):
        return '%s %s' % (self.nfc_email, self.nfkc_company_name)


""" POSTING MODEL  """
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

    employer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="related employer", blank=False, limit_choices_to={"is_employer":True})
    title = models.CharField(max_length=150, blank=False, db_index=True)
    work_title = models.CharField(max_length=50, blank=False, db_index=True)
    description = models.CharField(max_length=500, blank=False)
    work_type = models.CharField(max_length=2, choices=WORK_TYPE_CHOICES, default=FULLTIME)
    weekly_hours = models.IntegerField(blank=False)
    locally_bound = models.BooleanField(blank=False, default=True)
    city = models.CharField(max_length=50, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s || %s || %s' % (self.title, self.work_title, self.city)

""" APPLICATION MODEL """
class Application(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="related applicant", blank=True, null=True)
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE, verbose_name="related posting", blank=False)
    email = models.EmailField(blank=False)
    cover_letter = models.CharField(max_length=3000, blank=False)
    cv_link = models.URLField(max_length=800, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('posting', 'email')

    def __str__(self):
        return self.email





