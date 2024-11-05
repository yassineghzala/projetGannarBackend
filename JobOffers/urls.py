from django.urls import path, include

from JobOffers.views import JobOfferGP, JobOfferGPD, apply, getApplicationCandidates, getApplications, getJobOffersByRecruiter,getMatches, matchCandidateWithJobs

urlpatterns = [
    path('jobs', JobOfferGP),
    path('application/<int:CandidateId>/apply/<int:JobOfferId>', apply),
    path('jobs/<int:JobOfferId>', JobOfferGPD),
    path('matches/<int:CandidateId>', getMatches),
    path('applications/<int:CandidateId>', getApplications),
    path('jobs-history/<int:recruiterId>', getJobOffersByRecruiter),
    path('applicationCandidates/<int:JobOfferId>', getApplicationCandidates),
    path('matchCandidateWithJobs/<int:candidateId>', matchCandidateWithJobs)
]