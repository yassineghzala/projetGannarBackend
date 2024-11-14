from django.urls import path, include
from . import views
from JobOffers.views import JobOfferGP, JobOfferGPD, apply, deleteApplicationById, get_unread_notifications, getApplicationByCandidateIdAndJobOfferId, getApplicationCandidates, getApplications, getJobOffersByRecruiter,getMatches, mark_all_notifications_as_read, mark_notification_as_read, matchCandidateWithJobs

urlpatterns = [
    path('jobs', JobOfferGP),
     path('apply/<int:JobOfferId>/<int:CandidateId>', apply),
    path('jobs/<int:JobOfferId>', JobOfferGPD),
    path('matches/<int:CandidateId>', getMatches),
    path('getapplicationby/<int:candidateId>/and/<int:jobOfferId>', getApplicationByCandidateIdAndJobOfferId),
    path('applications/<int:CandidateId>', getApplications),
     path('applications/<int:applicationId>/delete', deleteApplicationById, name='delete_application_by_id'),
    path('jobs-history/<int:recruiterId>', getJobOffersByRecruiter),
    path('applicationCandidates/<int:JobOfferId>', getApplicationCandidates),
    path('matchCandidateWithJobs/<int:candidateId>', matchCandidateWithJobs, name='match_candidate_with_jobs'),
    path('notifications/unread/<int:recruiter_id>/', get_unread_notifications, name='get_unread_notifications'),
    path('notifications/mark-as-read/<int:notification_id>/', mark_notification_as_read, name='mark_notification_as_read'),
    path('notifications/mark-all-as-read/<int:recruiter_id>/', mark_all_notifications_as_read, name='mark_all_notifications_as_read'),
]