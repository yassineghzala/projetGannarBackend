from django.db import DatabaseError
from django.shortcuts import render, get_object_or_404
from Candidates.models import Candidate, Resume
from Candidates.serialisers import CandidateSerializer, ResumeSerializer
from Recruiters.models import Recruiter
from .models import Application, JobOffer, Match
from rest_framework.views import APIView
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from .serialisers import ApplicationSerializer, JobOfferSerializer, MatchSerializer
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.http import Http404

@api_view(['GET' , 'POST'])
def JobOfferGP(request):
    if(request.method == "GET"):
        jobOffers = JobOffer.objects.all()
        jobOffer_serializer = JobOfferSerializer(jobOffers, many=True)
        return JsonResponse(jobOffer_serializer.data,safe=False)
    elif(request.method == 'POST'):
        jobOffer_serializer = JobOfferSerializer(data=request.data)
        if jobOffer_serializer.is_valid():
            try:
                jobOffer_serializer.save()
                return Response(jobOffer_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response(jobOffer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET' , 'PUT' , 'DELETE'])
def JobOfferGPD(request,JobOfferId):
    try:
        jobOffer = get_object_or_404(JobOffer,pk=JobOfferId)
        jobOffer_serializer = JobOfferSerializer(jobOffer)
    except Http404:
        return Response(
            {"error": "No jobOffer with given Id exists"},
            status=status.HTTP_404_NOT_FOUND
            )
    
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

    try:
        jobOffer = get_object_or_404(JobOffer,pk=JobOfferId)
    except Http404:
        return Response(
            {"error": "No jobOffer with given Id exists"},
            status=status.HTTP_404_NOT_FOUND
            )
    try:
        candidate = get_object_or_404(Candidate,pk=CandidateId)
    except Http404:
        return Response(
            {"error": "No jobOffer with given Id exists"},
            status=status.HTTP_404_NOT_FOUND
            )
    try:
        cv = get_object_or_404(Resume,pk=candidate.cv_id)
    except Http404:
        return Response(
            {"error": "No jobOffer with given Id exists"},
            status=status.HTTP_404_NOT_FOUND
            )

    candidate_skills = cv.skills.split(',')
    job_skills = jobOffer.skills.split(',')

    try:
        applications = Application.objects.all()
    except DatabaseError:
        return Response(
            {"error": "Database error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception:
        return Response(
            {"error": "An unexpected error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    if(request.method == 'GET'):
        score = 0
        for candidateSkill in candidate_skills:
            for jobSkill in job_skills:
                if candidateSkill==jobSkill:
                    score = score + 1
        try:
            application = Application.objects.get(jobOffer=jobOffer,candidate=candidate)
            return Response(
                {"error": "Application already exists"},
                status=status.HTTP_409_CONFLICT
            )
        except Application.DoesNotExist:
            match_score = (score/len(job_skills) ) * 100  
            newApplication = Application(jobOffer=jobOffer,candidate=candidate,candidate_score=match_score)
            newApplication.save()
            return Response(
                {"message":"Application created with success"},
                status=status.HTTP_200_OK
            )

@api_view(['GET'])
def getMatches(request,CandidateId):
    if(request.method == 'GET'):
        try:
            get_object_or_404(Candidate,pk=CandidateId)
            candidateMatches = Match.objects.all().filter(candidate=CandidateId)
            match_serializer = MatchSerializer(candidateMatches,many=True)
            return JsonResponse(match_serializer.data,safe=False)
        except Http404:
            return Response(
                {"error": "No matches for candidate with given Id exists"},
                status=status.HTTP_404_NOT_FOUND               
            )
        except DatabaseError:
            return Response(
                {"error": "Database error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['GET'])
def getApplications(request,CandidateId):
    if(request.method == 'GET'):
        try:
            get_object_or_404(Candidate,pk=CandidateId)
            candidateApplications = Application.objects.all().filter(candidate=CandidateId)
            application_serializer = ApplicationSerializer(candidateApplications,many=True)
            return JsonResponse(application_serializer.data,safe=False) 
        except Http404:
            return Response(
                {"error": "No applications for candidate with given Id exists"},
                status=status.HTTP_404_NOT_FOUND               
            )
        except DatabaseError:
            return Response(
                {"error": "Database error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
@api_view(['GET'])
def getApplicationCandidates(request,JobOfferId):
    candidates = []
    if(request.method == 'GET'):
        try:
            get_object_or_404(JobOffer,pk=JobOfferId)
            candidateApplications = Application.objects.all().filter(jobOffer=JobOfferId)
            for c in candidateApplications:
                newCandidate = Candidate.objects.get(id=c.candidate.id)
                candidates.append(newCandidate)
            candidates_serializer = CandidateSerializer(candidates,many=True)
            return JsonResponse(candidates_serializer.data,safe=False)
        except Http404:
            return Response(
                {"error": "No applications for candidate with given Id exists"},
                status=status.HTTP_404_NOT_FOUND               
            )
        except DatabaseError:
            return Response(
                {"error": "Database error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )    
        
@api_view(['GET'])
def getJobOffersByRecruiter(request,recruiterId):
    if(request.method == 'GET'):
        try:
            get_object_or_404(Recruiter,pk=recruiterId)
            jobOffers = JobOffer.objects.all().filter(recruiter=recruiterId)
            jobOffers_serializer = JobOfferSerializer(jobOffers,many=True)
            return JsonResponse(jobOffers_serializer.data,safe=False)
        except Http404:
            return Response(
                {"error": "No applications for candidate with given Id exists"},
                status=status.HTTP_404_NOT_FOUND               
            )     
        except DatabaseError:
            return Response(
                {"error": "Database error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )  

@api_view(['POST'])
def matchCandidateWithJobs(request,candidateId):

    try:
        candidate = get_object_or_404(Candidate,pk=candidateId)
    except Http404:
        return Response(
                {"error": "No applications for candidate with given Id exists"},
                status=status.HTTP_404_NOT_FOUND   
        )

    try:
        cv = get_object_or_404(Resume,pk=candidate.cv_id)
    except Http404:
        return Response(
                {"error": "No applications for candidate with given Id exists"},
                status=status.HTTP_404_NOT_FOUND              
        )
    #matches = Match.objects.all()
    jobOffers = JobOffer.objects.all()

    candidate_skills = cv.skills.split(',')
    
    for job in jobOffers:
        job_skills = job.skills.split(',')
        score = 0
        for candidateSkill in candidate_skills:
            for jobSkill in job_skills:
                if candidateSkill == jobSkill:
                    score = score + 1;
        if(score!=0):
            try:
                match = Match.objects.get(jobOffer=job,candidate=candidate)
                print("Objects already exists",match)
                return Response(
                    {"error": "Match already exists"},
                    status=status.HTTP_409_CONFLICT
                )
            except Match.DoesNotExist:    
                match_score = (score/len(job_skills) ) * 100  
                newMatch = Match(jobOffer=job,candidate=candidate,candidate_score=match_score)
                print("Objects doesnt exists, a new match is created!") 
                newMatch.save()
                return Response(
                    {"message":"Application created with success"},
                    status=status.HTTP_200_OK
                )
        #matches_serializer = MatchSerializer(matches,many=True)
    #return JsonResponse(matches_serializer.data,safe=False) 