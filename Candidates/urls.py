from django.urls import path

from Candidates.views import CandidateGP, CandidateGPD
from JobOffers.views import JobOfferGP


urlpatterns = [
    path('candidates', CandidateGP),
    path('recruiters/<int:Id>', CandidateGPD)
]