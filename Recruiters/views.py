from django.shortcuts import render, get_object_or_404
from Recruiters.models import Recruiter
from rest_framework.views import APIView
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from .serialisers import RecruiterSerializer
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
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

