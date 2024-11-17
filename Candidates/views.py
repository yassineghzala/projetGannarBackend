from datetime import datetime, timedelta

from django.shortcuts import render, get_object_or_404
import jwt
from Candidates.models import Candidate, Resume
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serialisers import CandidateSerializer, ResumeSerializer
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status, serializers
from django.http import Http404
from django.db import DatabaseError

# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        try:
            email = request.data['email']
            print(email)
            candidate = Candidate.objects.get(email=email)
            return Response(
                {"error": "Candidate with this email already exists"},
                status=status.HTTP_409_CONFLICT
            )
        except Candidate.DoesNotExist:
            try:
                # Assign the role 'candidate' before saving
                request.data['role'] = 'candidate'
                serializer = CandidateSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(
                    {"message": "Candidate registered successfully"},
                    status=status.HTTP_201_CREATED
                )
            except serializers.ValidationError as e:
                return Response(
                    {"error": "Validation error", "details": e.detail},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except DatabaseError as e:
                return Response(
                    {"error": "Database error occurred while saving the candidate", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            except Exception as e:
                return Response(
                    {"error": "An unexpected error occurred", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except DatabaseError as e:
            return Response(
                {"error": "Database error occurred while fetching the candidate", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

def create_access_token(request):
    try:
        email = request.data['email']
        password = request.data['password']
        user = Candidate.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
        if user.password != password:
            raise AuthenticationFailed('Incorrect password!')
        payload = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'address': user.address,
            'phoneNumber': user.phoneNumber,
            'role': user.role,
            'dateOfBirth': user.dateOfBirth,
            'exp': datetime.utcnow() + timedelta(minutes=60),
            'iat': datetime.utcnow() - timedelta(hours=1)
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
        user = Candidate.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
        if user.password != password:
            raise AuthenticationFailed('Incorrect password!')
        payload = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'address': user.address,
            'phoneNumber': user.phoneNumber,
            'role': user.role,
            'dateOfBirth': user.dateOfBirth,
            'exp': datetime.utcnow() + timedelta(minutes=120),
            'iat': datetime.utcnow() - timedelta(hours=1)
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token
    except AuthenticationFailed as e:
        raise AuthenticationFailed(str(e))
    except Exception as e:
        raise Exception(str(e))

def VerifyToken(request):
    try:
        if(request.COOKIES.get('access') and request.COOKIES.get("refresh")):
            access_token = request.COOKIES.get('access')
            refresh_token = request.COOKIES.get("refresh")
            if isinstance(access_token, str) and isinstance(refresh_token, str):
                access_token = access_token.encode('utf-8') 
                refresh_token = refresh_token.encode('utf-8') 
            payload_access = jwt.decode(access_token,'secret', algorithms=["HS256"], options={"verify_signature": False})
            payload_refresh = jwt.decode(refresh_token,'secret',algorithms=["HS256"], options={"verify_signature": False})    
            if(payload_access == payload_refresh):
                return True
            else:
                return False
    except jwt.DecodeError as e:
        print("Token decode error:", e)
        return Response({'detail': 'Internal Server Error'}, status=500)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    def post(self, request):
        try:
            access_token = create_access_token(request)
            refresh_token = create_refresh_token(request)
            token = {'access_token': access_token, 'refresh_token': refresh_token}
            response = Response(data=token)
            response.set_cookie(key='access', value=access_token, httponly=True, samesite='None', secure=True)
            response.set_cookie(key='refresh', value=refresh_token, httponly=True, samesite='None', secure=True)
            return response
        except AuthenticationFailed as e:
            print("Authentication failed:", e)
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Logout(APIView):
    def get(self,request):
        try:
            response = Response()
            response.delete_cookie("access")
            response.delete_cookie("refresh")
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserView(APIView):
    def post(self, request):
        try:
            auth_header = request.headers.get('Authorization', '')
            token = request.COOKIES.get('access')
            print(request.COOKIES)
            if isinstance(token, str):
                token = token.encode('utf-8')  # Convert the string to bytes
            payload = jwt.decode(token,'secret', algorithms=["HS256"], options={"verify_signature": False})
            user = Candidate.objects.filter(id=payload['id']).first()
            serializer = CandidateSerializer(user)
            print(serializer.data)
            return Response(serializer.data)
        except jwt.DecodeError as e:
            print("Token decode error:", e)
            return Response({'detail': 'Internal Server Error'}, status=500)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET' , 'POST'])
def CandidateGP(request):
    try:
        if(request.method == "GET"):
            candidates = Candidate.objects.all()
            candidate_serializer = CandidateSerializer(candidates, many=True)
            return JsonResponse(candidate_serializer.data,safe=False)
        elif(request.method == 'POST'):
            candidate_serializer = CandidateSerializer(data=request.data)
            if candidate_serializer.is_valid():
                candidate_serializer.save()
            return JsonResponse(candidate_serializer.data,safe=False)
    except DatabaseError as e:
        return Response({'error': 'Database error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_candidate_by_id(request, candidate_id):
    try:
        candidate = get_object_or_404(Candidate, pk=candidate_id)
        serializer = CandidateSerializer(candidate)
        return Response(serializer.data)
    except Candidate.DoesNotExist:
        return Response({'error': 'Candidate not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET' , 'PUT' , 'DELETE'])
def CandidateGPD(request,Id):
    try:
        candidate = get_object_or_404(Candidate,pk=Id)
        candidate_serializer = CandidateSerializer(candidate)
        if(request.method == "PUT"):
            candidate_data = JSONParser().parse(request)
            candidate_serializer = CandidateSerializer(candidate,data=candidate_data)
            if(candidate_serializer.is_valid()):
                candidate_serializer.save()
                return JsonResponse(candidate_serializer.data)  
        elif(request.method == "DELETE"):
            candidate.delete()
        return JsonResponse(candidate_serializer.data)
    except Candidate.DoesNotExist:
        return Response({'error': 'Candidate not found'}, status=404)
    except DatabaseError as e:
        return Response({'error': 'Database error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_recommended_candidates(request):
    try:
        candidates = Candidate.objects.filter(cv__res_score__gt=50)
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def getCVByCandidateId(request,candidateId):
    try:
        if(request.method=='GET'):
            candidate = get_object_or_404(Candidate,pk=candidateId)
            print(candidate.cv)
            CV = candidate.cv
            CV_serializer = ResumeSerializer(CV)
            return JsonResponse(CV_serializer.data,safe=False)
    except Candidate.DoesNotExist:
        return Response({'error': 'Candidate not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)