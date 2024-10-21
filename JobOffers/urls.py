from django.urls import path, include

from JobOffers.views import JobOfferGP, JobOfferGPD, apply, getApplications, getMatches, matchCandidateWithJobs

urlpatterns = [
    path('jobs', JobOfferGP),
    path('application/<int:CandidateId>/apply/<int:JobOfferId>', apply),
    path('jobs/<int:JobOfferId>', JobOfferGPD),
    path('matches/<int:CandidateId>', getMatches),
    path('applications/<int:CandidateId>', getApplications),
    path('matchCandidateWithJobs/<int:candidateId>', matchCandidateWithJobs)
]