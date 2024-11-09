from rest_framework import serializers
from .models import Candidate, Resume
class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = [
            'id',
            'email',
            'name',
            'password',
            'address',
            'phoneNumber',
            'dateOfBirth',
            'cv'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
        def create(self, validated_data):
            password = validated_data.pop('password', None)
            instance = self.Meta.model(**validated_data)
            if password is not None:
                instance.set_password(password)
            instance.save()
            return instance
        
class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = [
            'Id',
            'file',
            'skills'
        ]