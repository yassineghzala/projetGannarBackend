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
            'role',
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
            'sec_token',
            'ip_add',
            'host_name',
            'dev_user',
            'os_name_ver',
            'latlong',
            'city',
            'state',
            'country',
            'act_name',
            'act_mail',
            'act_mob',
            'name',
            'email',
            'res_score',
            'timestamp',
            'no_of_pages',
            'reco_field',
            'cand_level',
            'skills',
            'recommended_skills',
            'courses',
            'pdf_name'
        ]