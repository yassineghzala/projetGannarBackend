from rest_framework import serializers
from .models import Recruiter
class RecruiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiter
        fields = [
            'Id',
            'name',
            'email',
        ]