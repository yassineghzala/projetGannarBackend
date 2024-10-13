from rest_framework import serializers

from JobOffers.models import Application, JobOffer, Match
class JobOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOffer
        fields = [
            'Id',
            'details'
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            'Id',
            'candidate',
            'jobOffer'
        ]


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = [
            'Id',
            'candidate',
            'jobOffer'
        ]