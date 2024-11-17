from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404
import jwt
from Candidates.models import Candidate
from Candidates.serialisers import CandidateSerializer
from JobOffers.models import JobOffer, Application
from JobOffers.serialisers import JobOfferSerializer
from Recruiters.models import Recruiter
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serialisers import RecruiterSerializer
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status, serializers
from django.db import DatabaseError

# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        try:
            email = request.data['email']
            print(email)
            recruiter = Recruiter.objects.get(email=email)
            return Response(
                {"error": "Recruiter with this email already exists"},
                status=status.HTTP_409_CONFLICT
            )
        except Recruiter.DoesNotExist:
            try:
                serializer = RecruiterSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(
                    {"message": "Recruiter registered successfully"},
                    status=status.HTTP_201_CREATED
                )
            except serializers.ValidationError as e:
                return Response(
                    {"error": "Validation error", "details": e.detail},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except DatabaseError as e:
                return Response(
                    {"error": "Database error occurred while saving the recruiter", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            except Exception as e:
                return Response(
                    {"error": "An unexpected error occurred", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except DatabaseError as e:
            return Response(
                {"error": "Database error occurred while fetching the recruiter", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['GET', 'POST'])
def RecruiterGP(request):
    try:
        if request.method == "GET":
            recruiters = Recruiter.objects.all()
            recruiter_serializer = RecruiterSerializer(recruiters, many=True)
            return JsonResponse(recruiter_serializer.data, safe=False)
        elif request.method == 'POST':
            recruiter_serializer = RecruiterSerializer(data=request.data)
            if recruiter_serializer.is_valid():
                recruiter_serializer.save()
            return JsonResponse(recruiter_serializer.data, safe=False)
    except DatabaseError as e:
        return Response({'error': 'Database error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'PUT', 'DELETE'])
def RecruiterGPD(request, Id):
    try:
        recruiter = get_object_or_404(Recruiter, pk=Id)
        recruiter_serializer = RecruiterSerializer(recruiter)
        if request.method == "GET":
            return JsonResponse(recruiter_serializer.data)
        elif request.method == "PUT":
            recruiter_data = JSONParser().parse(request)
            recruiter_serializer = RecruiterSerializer(recruiter, data=recruiter_data)
            if recruiter_serializer.is_valid():
                recruiter_serializer.save()
                return JsonResponse(recruiter_serializer.data)
        elif request.method == "DELETE":
            recruiter.delete()
        return JsonResponse(recruiter_serializer.data)
    except Recruiter.DoesNotExist:
        return Response({'error': 'Recruiter not found'}, status=404)
    except DatabaseError as e:
        return Response({'error': 'Database error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def getCandidatesByRecruiterId(request, recruiterId):
    try:
        job_offers = JobOffer.objects.filter(recruiter_id=recruiterId)
        result = []
        for job_offer in job_offers:
            applications = Application.objects.filter(jobOffer=job_offer)
            candidates = Candidate.objects.filter(id__in=applications.values_list('candidate_id', flat=True)).distinct()
            candidate_serializer = CandidateSerializer(candidates, many=True)
            job_offer_serializer = JobOfferSerializer(job_offer)
            result.append({
                'job_offer': job_offer_serializer.data,
                'candidates': candidate_serializer.data
            })
        return JsonResponse(result, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def create_access_token(request):
    try:
        email = request.data['email']
        password = request.data['password']
        user = Recruiter.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
        if user.password != password:
            raise AuthenticationFailed('Incorrect password!')
        payload = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'exp': datetime.now() + timedelta(minutes=60),
            'iat': datetime.now()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token
    except AuthenticationFailed as e:
        raise AuthenticationFailed(str(e))
    except Exception as e:
        raise Exception(str(e))

def create_refresh_token(request):
    try:
        email = request.data['email']
        password = request.data['password']
        user = Recruiter.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
        if user.password != password:
            raise AuthenticationFailed('Incorrect password!')
        payload = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'exp': datetime.now() + timedelta(minutes=120),
            'iat': datetime.now()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token
    except AuthenticationFailed as e:
        raise AuthenticationFailed(str(e))
    except Exception as e:
        raise Exception(str(e))

class LoginView(APIView):
    def post(self, request):
        try:
            access_token = create_access_token(request)
            refresh_token = create_refresh_token(request)
            token = {'access_token': access_token, 'refresh_token': refresh_token}
            response = Response(data=token)
            response.set_cookie(key='access', value=access_token, httponly=True)
            response.set_cookie(key='refresh', value=refresh_token, httponly=True)
            return response
        except AuthenticationFailed as e:
            print("Authentication failed:", e)
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)