from django.shortcuts import render, get_object_or_404
from Candidates.models import Candidate
from rest_framework.views import APIView
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from .serialisers import CandidateSerializer
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
# Create your views here.

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
    if(request.method == "GET"):
        return JsonResponse(candidate_serializer.data) 
    elif(request.method == "PUT"):
        candidate_data = JSONParser().parse(request)
        candidate_serializer = CandidateSerializer(candidate,data=candidate_data)
        if(candidate_serializer.is_valid()):
            candidate_serializer.save()
            return JsonResponse(candidate_serializer.data)  
    elif(request.method == "DELETE"):
        candidate.delete();
    return JsonResponse(candidate_serializer.data)

