from rest_framework import serializers
from .models import User, Posting, Application

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'is_employer', 'is_active', 'company_name']

    def validate(self, data):
        """
        Check that employers fill out company name
        """
        if data['is_employer'] == True and data['company_name'] == "":
            raise serializers.ValidationError("Employers must fill out company name")
        return data

class PostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posting
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

