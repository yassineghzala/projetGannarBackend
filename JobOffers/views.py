from django.shortcuts import render, get_object_or_404
from Candidates.models import Candidate, Resume
from Candidates.serialisers import ResumeSerializer
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


@api_view(['GET'])
def apply(request,JobOfferId,CandidateId):
    jobOffer = get_object_or_404(JobOffer,pk=JobOfferId)
    candidate = get_object_or_404(Candidate,pk=CandidateId)

    cv = get_object_or_404(Resume,pk=candidate.cv_id)

    candidate_skills = cv.skills.split(',')
    job_skills = jobOffer.skills.split(',')

    applications = Application.objects.all()

    if(request.method == 'GET'):
        score = 0
        for candidateSkill in candidate_skills:
            for jobSkill in job_skills:
                if candidateSkill==jobSkill:
                    score = score + 1
        try:
            application = Application.objects.get(jobOffer=jobOffer,candidate=candidate)
            print("Objects already exists",application)

        except Application.DoesNotExist:
            match_score = (score/len(job_skills) ) * 100  
            newApplication = Application(jobOffer=jobOffer,candidate=candidate,candidate_score=match_score)
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


@api_view(['POST'])
def matchCandidateWithJobs(request,candidateId):

    matches = Match.objects.all()

    jobOffers = JobOffer.objects.all()
    candidate = get_object_or_404(Candidate,pk=candidateId)

    cv = get_object_or_404(Resume,pk=candidate.cv_id)
    
    candidate_skills = cv.skills.split(',')
    
    for job in jobOffers:
        job_skills = job.skills.split(',')
        score = 0
        for candidateSkill in candidate_skills:
            for jobSkill in job_skills:
                if candidateSkill == jobSkill:
                    score = score + 1;
        #print(f'candidate skills: ',candidate_skills)
        #print(f'job skills: ',job_skills)
        #print(job)
        #print(candidate)
        #print(score)
        if(score!=0):
            try:
                match = Match.objects.get(jobOffer=job,candidate=candidate)
                print("Objects already exists",match)
            except Match.DoesNotExist:    
                match_score = (score/len(job_skills) ) * 100  
                newMatch = Match(jobOffer=job,candidate=candidate,candidate_score=match_score)
                print("Objects doesnt exists, a new match is created!") 
                newMatch.save() 
        matches_serializer = MatchSerializer(matches,many=True)
    return JsonResponse(matches_serializer.data,safe=False) 


        