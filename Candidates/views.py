from datetime import datetime, timedelta

from django.shortcuts import render, get_object_or_404
import jwt
from Candidates.models import Candidate, Resume
from rest_framework.views import APIView
from rest_framework.decorators import api_view ,parser_classes
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
from rest_framework import status
from django.http import Http404
# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        try:
            email = request.data['email']
            print(email)
            candidate = Candidate.objects.get(email=email)
            return Response(
                {"error": "candidate with email already exists"},
                status=status.HTTP_409_CONFLICT
            )
        except Candidate.DoesNotExist:
                serializer = CandidateSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(
                    {"message": "candidate registered with success"},
                    status=status.HTTP_200_OK
                )
def create_access_token(request):
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
    #response.set_cookie(key='access_token', value=token, httponly=True)
    return token

def create_refresh_token(request):
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

def VerifyToken(request):
    if(request.COOKIES.get('access') and request.COOKIES.get("refresh")):
        access_token = request.COOKIES.get('access')
        refresh_token = request.COOKIES.get("refresh")
        try:
            if isinstance(access_token, str) and isinstance(refresh_token, str):
                access_token = access_token.encode('utf-8') 
                refresh_token = refresh_token.encode('utf-8') 
            payload_access = jwt.decode(access_token,'secret', algorithms=["HS256"], options={"verify_signature": False})
            payload_refresh = jwt.decode(refresh_token,'secret',algorithms=["HS256"], options={"verify_signature": False})    
            if(payload_access == payload_refresh):
                return True
            else:
                return False
            #user = Candidate.objects.filter(id=payload_access['id']).first()
            #serializer = CandidateSerializer(user)
            #print(serializer.data)
            #return Response(serializer.data)
    
        except jwt.DecodeError as e:
            print("Token decode error:", e)
            return Response({'detail': 'Internal Server Error'}, status=500)

class LoginView(APIView):
    def post(self,request):
        access_token = create_access_token(request)
        refresh_token = create_refresh_token(request)
        token = {'access_token': access_token,'refresh_token': refresh_token}
        response = Response(data=token) 
        response.set_cookie(key='access', value=access_token, httponly=True,samesite='None',secure=True)
        response.set_cookie(key='refresh', value=refresh_token, httponly=True,samesite='None',secure=True)
        return response
    
class Logout(APIView):
    def get(self,request):
        response = Response()
        response.delete_cookie("access")
        response.delete_cookie("refresh")

#class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#    @classmethod
#    def get_token(cls, user):
#        token = super().get_token(user)
#        token['id'] = user.id
#        token['name'] = user.name
#        token['email'] = user.email
#
#        return token
#
#class MyTokenObtainPairView(TokenObtainPairView):
#    serializer_class = MyTokenObtainPairSerializer
#
#    def post(self, request):  
#        email = request.data.get('email')
#        password = request.data.get('password')
#        candidate = Candidate.objects.get(email=email)
#        print(candidate.password)
#        if candidate and (candidate.password == password):
#
#            token = self.serializer_class.get_token(candidate)
#
#            access_token = str(token.access_token)
#            refresh_token = str(token)
#
#            response = Response()
#            response.data = {
#                'access_token': access_token,
#                'refresh_token': refresh_token
#            }
#            response.set_cookie(key='jwt', value=refresh_token, httponly=True,secure=True,samesite='None')
#            return response
#        return Response({'detail': 'Invalid credentials'}, status=400)
#    
class UserView(APIView):
    
    def post(self, request):
        auth_header = request.headers.get('Authorization', '')
        token = request.COOKIES.get('access')

        print(request.COOKIES)
        try:
            # Ensure token is in bytes format
            if isinstance(token, str):
                token = token.encode('utf-8')  # Convert the string to bytes
            
            payload = jwt.decode(token,'secret', algorithms=["HS256"], options={"verify_signature": False})
            
            user = Candidate.objects.filter(id=payload['id']).first()
            serializer = CandidateSerializer(user)
            print(serializer.data)
            return Response(serializer.data)
        
        except jwt.DecodeError as e:
            print("Token decode error:", e)
            return Response({'detail': 'AAInternal Server Error'}, status=500)
            
    
@api_view(['GET' , 'POST'])
def CandidateGP(request):
    if(request.method == "GET"):
        candidates = Candidate.objects.all()
        candidate_serializer = CandidateSerializer(candidates, many=True)
        return JsonResponse(candidate_serializer.data,safe=False)
    elif(request.method == 'POST'):
        candidate_serializer = CandidateSerializer(data=request.data)
        if candidate_serializer.is_valid():
            candidate_serializer.save()
        return JsonResponse(candidate_serializer.data,safe=False)

@api_view(['GET' , 'PUT' , 'DELETE'])
def CandidateGPD(request,Id):
    candidate = get_object_or_404(Candidate,pk=Id)
    candidate_serializer = CandidateSerializer(candidate)
    if(request.method == "PUT"):
        candidate_data = JSONParser().parse(request)
        candidate_serializer = CandidateSerializer(candidate,data=candidate_data)
        if(candidate_serializer.is_valid()):
            candidate_serializer.save()
            return JsonResponse(candidate_serializer.data)  
    elif(request.method == "DELETE"):
        candidate.delete();
    return JsonResponse(candidate_serializer.data)

@api_view(['GET'])
def getCVByCandidateId(request,candidateId):
    if(request.method=='GET'):
        candidate = get_object_or_404(Candidate,pk=candidateId)
        print(candidate.cv)
        CV = candidate.cv
        #CV = get_object_or_404(Resume,pk=CV_id)
        CV_serializer = ResumeSerializer(CV)
        return JsonResponse(CV_serializer.data,safe=False)

