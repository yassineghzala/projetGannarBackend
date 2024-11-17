from rest_framework import serializers

from JobOffers.models import Application, JobOffer, Match
class JobOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOffer
        fields = [
            'Id',
            'recruiter',
            'name',
            'description',
            'workTime',
            'salary',
            'skills',
            'company',
            'email',
            'numtel',
            'location',
            'expirationDate'
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            'Id',
            'candidate',
            'jobOffer',
            'candidate_score'
        ]


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = [
            'Id',
            'candidate',
            'jobOffer',
            'candidate_score',
            'matchedSkills'
        ]