from django.urls import path, include

from JobOffers.views import JobOfferGPD, apply, getApplications, getMatches

urlpatterns = [
    path('application/<int:CandidateId>/apply/<int:JobOfferId>', apply),
    path('singleJobOffer/<int:JobOfferId>', JobOfferGPD),
    path('matches/<int:CandidateId>', getMatches),
    path('applications/<int:CandidateId>', getApplications),
]