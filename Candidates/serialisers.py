from rest_framework import serializers
from .models import Candidate, Resume
class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = [
            'Id',
            'name',
            'email',
            'cv'
        ]
class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = [
            'Id',
            'file',
            'skills'
        ]