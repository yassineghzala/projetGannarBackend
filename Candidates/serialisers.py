from rest_framework import serializers
from .models import Candidate
class RecruiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = [
            'Id',
            'name',
            'email',
        ]