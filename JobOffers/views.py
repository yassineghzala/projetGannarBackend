from django.shortcuts import render, get_object_or_404
from Candidates.models import Candidate
from Recruiters.models import Recruiter
from .models import Application, JobOffer, Match
from rest_framework.views import APIView
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from .serialisers import ApplicationSerializer, JobOfferSerializer, MatchSerializer
from django.http import JsonResponse
from rest_framework.parsers import JSONParser


@api_view(['GET' , 'POST'])
def JobOfferGP(request):
    if(request.method == "GET"):
        jobOffers = JobOffer.objects.all()
        jobOffer_serializer = JobOfferSerializer(jobOffers, many=True)
        return JsonResponse(jobOffer_serializer.data,safe=False)
    elif(request.method == 'POST'):
        jobOffer_serializer = JobOfferSerializer(data=request.data)
        if jobOffer_serializer.is_valid():
            jobOffer_serializer.save()
        return JsonResponse(jobOffer_serializer.data,safe=False)


@api_view(['GET' , 'PUT' , 'DELETE'])
def JobOfferGPD(request,JobOfferId):
    jobOffer = get_object_or_404(JobOffer,pk=JobOfferId)
    jobOffer_serializer = JobOfferSerializer(jobOffer)
    if(request.method == "GET"):
        return JsonResponse(jobOffer_serializer.data) 
    elif(request.method == "PUT"):
        jobOffer_data = JSONParser().parse(request)
        jobOffer_serializer = JobOfferSerializer(jobOffer,data=jobOffer_data)
        if(jobOffer_serializer.is_valid()):
            jobOffer_serializer.save()
            return JsonResponse(jobOffer_serializer.data)  
    elif(request.method == "DELETE"):
        jobOffer.delete();
    return JsonResponse(jobOffer_serializer.data)


@api_view(['POST'])
def apply(request,JobOfferId,CandidateId):
    jobOffer = get_object_or_404(JobOffer,pk=JobOfferId)
    candidate = get_object_or_404(Candidate,pk=CandidateId)
    applications = Application.objects.all()
    if(request.method == 'POST'):
        try:
            application = Application.objects.get(jobOffer=jobOffer,candidate=candidate)
            print("Objects already exists",application)

        except Application.DoesNotExist:
            newApplication = Application(jobOffer=jobOffer,candidate=candidate)
            newApplication.save()
            print("Objects doesnt exists, a new application is created!")

        applications_serializer = ApplicationSerializer(applications,many=True)
        return JsonResponse(applications_serializer.data,safe=False) 


@api_view(['GET'])
def getMatches(request,CandidateId):
    if(request.method == 'GET'):
        candidateMatches = Match.objects.all().filter(candidate=CandidateId)
        match_serializer = MatchSerializer(candidateMatches,many=True)
        return JsonResponse(match_serializer.data,safe=False) 
@api_view(['GET'])
def getApplications(request,CandidateId):
    if(request.method == 'GET'):
        candidateApplications = Application.objects.all().filter(candidate=CandidateId)
        application_serializer = ApplicationSerializer(candidateApplications,many=True)
        return JsonResponse(application_serializer.data,safe=False) 


        