from rest_framework import serializers
from .models import Recruiter
class RecruiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiter
        fields = [
            'id',
            'name',
            'email',
            'password',
            'company',
            'companyAddress',
            'domain',
            'post',
            'phoneNumber'
        ]
# class NotificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Notification
#         fields = [
#             'id',
#             'message',
#             'date',
#             'recruiter',
#         ]