from django.db import DatabaseError
from django.shortcuts import render, get_object_or_404
from Candidates.models import Candidate, Resume
from Candidates.serialisers import CandidateSerializer, ResumeSerializer
from Candidates.views import VerifyToken
from Recruiters.models import Recruiter
from .models import Application, JobOffer, Match, Notification
from rest_framework.views import APIView
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from .serialisers import ApplicationSerializer, JobOfferSerializer, MatchSerializer
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.http import Http404
from django.views.decorators.http import require_http_methods

@api_view(['GET' , 'POST'])
def JobOfferGP(request):
    if request.method == "GET":
        try:
            jobOffers = JobOffer.objects.all()
            jobOffer_serializer = JobOfferSerializer(jobOffers, many=True)
            return JsonResponse(jobOffer_serializer.data, safe=False)
        except DatabaseError:
            return Response(
                {"error": "Database error occurred while fetching job offers."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    elif request.method == 'POST':
        jobOffer_serializer = JobOfferSerializer(data=request.data)
        if jobOffer_serializer.is_valid():
            try:
                jobOffer_serializer.save()
                return Response(jobOffer_serializer.data, status=status.HTTP_201_CREATED)
            except DatabaseError:
                return Response(
                    {"error": "Database error occurred while saving the job offer."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            except Exception as e:
                return Response(
                    {"error": f"An unexpected error occurred: {str(e)}"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(jobOffer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET' , 'PUT' , 'DELETE'])
def JobOfferGPD(request, JobOfferId):
    try:
        jobOffer = get_object_or_404(JobOffer, pk=JobOfferId)
    except Http404:
        return Response(
            {"error": "No job offer with the given ID exists"},
            status=status.HTTP_404_NOT_FOUND
        )
    except DatabaseError:
        return Response(
            {"error": "Database error occurred while fetching the job offer."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    if request.method == "GET":
        try:
            jobOffer_serializer = JobOfferSerializer(jobOffer)
            return JsonResponse(jobOffer_serializer.data)
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    elif request.method == "PUT":
        try:
            jobOffer_data = JSONParser().parse(request)
            jobOffer_serializer = JobOfferSerializer(jobOffer, data=jobOffer_data)
            if jobOffer_serializer.is_valid():
                jobOffer_serializer.save()
                return JsonResponse(jobOffer_serializer.data)
            return Response(jobOffer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError:
            return Response(
                {"error": "Database error occurred while updating the job offer."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    elif request.method == "DELETE":
        try:
            jobOffer.delete()
            return JsonResponse({"message": "Job offer deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except DatabaseError:
            return Response(
                {"error": "Database error occurred while deleting the job offer."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['GET'])
def getApplicationByCandidateIdAndJobOfferId(request, candidateId, jobOfferId):
    try:
        application = Application.objects.get(jobOffer=jobOfferId, candidate=candidateId)
        application_serializer = ApplicationSerializer(application, many=False)
        return JsonResponse(application_serializer.data, safe=False)
    except Application.DoesNotExist:
        return Response(
            {"message": "Application not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    except DatabaseError:
        return Response(
            {"error": "Database error occurred while fetching the application."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def apply(request, JobOfferId, CandidateId):
    try:
        jobOffer = get_object_or_404(JobOffer, pk=JobOfferId)
    except Http404:
        return Response(
            {"error": "No job offer with the given ID exists"},
            status=status.HTTP_404_NOT_FOUND
        )
    except DatabaseError:
        return Response(
            {"error": "Database error occurred while fetching the job offer."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    try:
        candidate = get_object_or_404(Candidate, pk=CandidateId)
    except Http404:
        return Response(
            {"error": "No candidate with the given ID exists"},
            status=status.HTTP_404_NOT_FOUND
        )
    except DatabaseError:
        return Response(
            {"error": "Database error occurred while fetching the candidate."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    try:
        cv = get_object_or_404(Resume, pk=candidate.cv_id)
    except Http404:
        return Response(
            {"error": "No resume with the given ID exists"},
            status=status.HTTP_404_NOT_FOUND
        )
    except DatabaseError:
        return Response(
            {"error": "Database error occurred while fetching the resume."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    candidate_skills = set(skill.lower() for skill in cv.skills.strip('[]').replace("'", "").split(', '))
    job_skills = set(skill.lower() for skill in jobOffer.skills.split(','))

    try:
        if Application.objects.filter(jobOffer=jobOffer, candidate=candidate).exists():
            return Response(
                {"error": "Application already exists"},
                status=status.HTTP_409_CONFLICT
            )
    except DatabaseError:
        return Response(
            {"error": "Database error occurred while checking for existing applications."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    matched_skills = candidate_skills.intersection(job_skills)
    match_score = (len(matched_skills) / len(job_skills)) * 100 if job_skills else 0

    try:
        newApplication = Application(jobOffer=jobOffer, candidate=candidate, candidate_score=match_score)
        newApplication.save()
        return Response(
            {"message": "Application created successfully"},
            status=status.HTTP_201_CREATED
        )
    except DatabaseError:
        return Response(
            {"error": "Database error occurred while saving the application."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
@api_view(["GET"])
def get_unread_notifications(request, recruiter_id):
    try:
        unread_notifications = Notification.objects.filter(recruiter_id=recruiter_id, read_status=False)
        data = [{"id": n.id, "content": n.content, "created_at": n.created_at} for n in unread_notifications]
        return JsonResponse(data, safe=False)
    except DatabaseError:
        return Response(
            {"error": "Database error occurred while fetching unread notifications."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
def mark_notification_as_read(request, notification_id):
    try:
        notification = get_object_or_404(Notification, id=notification_id)
        notification.read_status = True
        notification.save()
        return JsonResponse({"message": "Notification marked as read"})
    except Http404:
        return Response(
            {"error": "Notification not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    except DatabaseError:
        return Response(
            {"error": "Database error occurred while updating the notification."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
def mark_all_notifications_as_read(request, recruiter_id):
    try:
        recruiter = get_object_or_404(Recruiter, id=recruiter_id)
        unread_notifications = Notification.objects.filter(recruiter=recruiter, read_status=False)
        unread_notifications.update(read_status=True)
        return JsonResponse({"message": "All notifications marked as read for this recruiter."})
    except Http404:
        return Response(
            {"error": "Recruiter not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    except DatabaseError:
        return Response(
            {"error": "Database error occurred while updating notifications."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def getMatches(request, CandidateId):
    try:
        candidate = get_object_or_404(Candidate, pk=CandidateId)
        candidateMatches = Match.objects.filter(candidate=candidate)
        match_serializer = MatchSerializer(candidateMatches, many=True)
        return JsonResponse(match_serializer.data, safe=False)
    except Http404:
        return Response(
            {"error": "No matches for candidate with the given ID exist"},
            status=status.HTTP_404_NOT_FOUND
        )
    except DatabaseError:
        return Response(
            {"error": "Database error occurred while fetching matches."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def getApplications(request, CandidateId):
    try:
        candidate = get_object_or_404(Candidate, pk=CandidateId)
        candidateApplications = Application.objects.filter(candidate=candidate)
        application_serializer = ApplicationSerializer(candidateApplications, many=True)
        return JsonResponse(application_serializer.data, safe=False)
    except Http404:
        return Response(
            {"error": "No applications for candidate with the given ID exist"},
            status=status.HTTP_404_NOT_FOUND
        )
    except DatabaseError:
        return Response(
            {"error": "Database error occurred while fetching applications."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def getApplicationCandidates(request, JobOfferId):
    try:
        jobOffer = get_object_or_404(JobOffer, pk=JobOfferId)
        candidateApplications = Application.objects.filter(jobOffer=jobOffer)
        candidates = [Candidate.objects.get(id=c.candidate.id) for c in candidateApplications]
        candidates_serializer = CandidateSerializer(candidates, many=True)
        return JsonResponse(candidates_serializer.data, safe=False)
    except Http404:
        return Response(
            {"error": "No job offer with the given ID exists"},
            status=status.HTTP_404_NOT_FOUND
        )
    except DatabaseError:
        return Response(
            {"error": "Database error occurred while fetching candidates."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['DELETE'])
def deleteApplicationById(request, applicationId):
    try:
        application = get_object_or_404(Application, pk=applicationId)
        application.delete()
        return JsonResponse({"message": "Application deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except Http404:
        return JsonResponse({"error": "Application not found."}, status=status.HTTP_404_NOT_FOUND)
    except DatabaseError:
        return JsonResponse({"error": "Database error occurred while deleting the application."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def getJobOffersByRecruiter(request, recruiterId):
    try:
        recruiter = get_object_or_404(Recruiter, pk=recruiterId)
        jobOffers = JobOffer.objects.filter(recruiter=recruiter)
        jobOffers_serializer = JobOfferSerializer(jobOffers, many=True)
        return JsonResponse(jobOffers_serializer.data, safe=False)
    except Http404:
        return Response(
            {"error": "No recruiter with the given ID exists"},
            status=status.HTTP_404_NOT_FOUND
        )
    except DatabaseError:
        return Response(
            {"error": "Database error occurred while fetching job offers."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def matchCandidateWithJobs(request,candidateId):

    try:
        candidate = Candidate.objects.get(pk=candidateId)
        cv = get_object_or_404(Resume, pk=candidate.cv_id)
        candidate_skills = set(skill.lower() for skill in cv.skills.strip('[]').replace("'", "").split(', '))
        job_offers = JobOffer.objects.all()
        matches = []

        for job in job_offers:
            if Match.objects.filter(candidate=candidate, jobOffer=job).exists():
                continue
            job_skills = set(skill.lower() for skill in job.skills.split(','))
            matched_skills = candidate_skills.intersection(job_skills)
            if matched_skills:
                match_score = (len(matched_skills) / len(job_skills)) * 100
                matched_skills_str = ','.join(matched_skills)
                new_match = Match(
                    jobOffer=job,
                    candidate=candidate,
                    candidate_score=match_score,
                    matchedSkills=matched_skills_str
                )
                new_match.save()
                matches.append(new_match)

        matches_serializer = MatchSerializer(matches, many=True)
        return JsonResponse(matches_serializer.data, safe=False)
    except Candidate.DoesNotExist:
        return JsonResponse({'error': 'Candidate not found'}, status=404)
    except DatabaseError:
        return JsonResponse({'error': 'Database error occurred while matching candidate with jobs.'}, status=500)
    except Exception as e:
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)