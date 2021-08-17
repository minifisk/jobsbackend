from rest_framework import serializers
from .models import User, Posting, Application

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nfkc_email', 'is_employer', 'is_active', 'nfkc_company_name']

    def validate(self, data):
        """
        Check that employers fill out company name
        """
        if data.get('is_employer') == True and data.get('nfkc_company_name') == "":
            raise serializers.ValidationError("Employers must fill out company name")
        if data.get('is_employer') == False and data.get('nfkc_company_name') != "":
            raise serializers.ValidationError("Only Employers can have a company name!")
        return data

class PostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posting
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['applicant', 'posting', 'email', 'cover_letter', 'cv_link']

