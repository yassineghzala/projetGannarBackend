from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404
import jwt
from Candidates.models import Candidate
from JobOffers.models import JobOffer
from Recruiters.models import Notification, Recruiter
from rest_framework.views import APIView
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from .serialisers import NotificationSerializer, RecruiterSerializer
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import AuthenticationFailed
from datetime import datetime
from django.http import Http404
from rest_framework import status
# Create your views here.

@api_view(['GET' , 'POST'])
def RecruiterGP(request):
    if(request.method == "GET"):
        recruiters = Recruiter.objects.all()
        recruiter_serializer = RecruiterSerializer(recruiters, many=True)
        return JsonResponse(recruiter_serializer.data,safe=False)
    elif(request.method == 'POST'):
        recruiter_serializer = RecruiterSerializer(data=request.data)
        if recruiter_serializer.is_valid():
            recruiter_serializer.save()
        return JsonResponse(recruiter_serializer.data,safe=False)

@api_view(['GET' , 'PUT' , 'DELETE'])
def RecruiterGPD(request,Id):
    recruiter = get_object_or_404(Recruiter,pk=Id)
    recruiter_serializer = RecruiterSerializer(recruiter)
    if(request.method == "GET"):
        return JsonResponse(recruiter_serializer.data) 
    elif(request.method == "PUT"):
        recruiter_data = JSONParser().parse(request)
        recruiter_serializer = RecruiterSerializer(recruiter,data=recruiter_data)
        if(recruiter_serializer.is_valid()):
            recruiter_serializer.save()
            return JsonResponse(recruiter_serializer.data)  
    elif(request.method == "DELETE"):
        recruiter.delete();
    return JsonResponse(recruiter_serializer.data)



@api_view(['POST','GET'])
def notifyRecruiter(request,recruiterId,jobOfferId,candidateId):

    jobOffer = get_object_or_404(JobOffer,pk=jobOfferId)
    candidate = get_object_or_404(Candidate,pk=candidateId)

    if(request.method == 'POST'):
        notification = Notification(recruiter=recruiterId,message="candidate ${candidate.name} has applied for job ${jobOffer.name}",date=datetime.now(),id=0)
        notification_serializer = NotificationSerializer(data=request.data)
        if notification_serializer.is_valid():
            notification_serializer.save()
        return JsonResponse(notification_serializer.data,safe=False)
    
    elif(request.method=='GET'):
        notifications = Notification.objects.all()
        notification_serializer = NotificationSerializer(notifications, many=True)
        return JsonResponse(notification_serializer.data,safe=False)
    



@api_view(['DELETE'])
def deleteNotification(request,notificationId):
    notifications = Notification.objects.all()
    notification_serializer = NotificationSerializer(notifications, many=True)
    try:
        notification = get_object_or_404(Notification,pk=notificationId)
        notification.delete()
        return JsonResponse(notification_serializer.data,safe=False)
    except Http404:
        return Response(
            {"error": "No notification with given Id exists"},
            status=status.HTTP_404_NOT_FOUND
            ) 

def create_access_token(request):
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
    #response.set_cookie(key='access_token', value=token, httponly=True)
    return token

def create_refresh_token(request):
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

class LoginView(APIView):
    def post(self,request):
        access_token = create_access_token(request)
        refresh_token = create_refresh_token(request)
        token = {'access_token': access_token,'refresh_token': refresh_token}
        response = Response(data=token) 
        response.set_cookie(key='access', value=access_token, httponly=True)
        response.set_cookie(key='refresh', value=refresh_token, httponly=True)
        return response
    
