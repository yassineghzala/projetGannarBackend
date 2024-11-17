from django.urls import path

from Candidates.views import CandidateGP, CandidateGPD, RegisterView
from JobOffers.views import JobOfferGP
from .views import LoginView, UserView, get_candidate_by_id, get_recommended_candidates, getCVByCandidateId

from rest_framework_simplejwt.views import (

    TokenRefreshView,
)

urlpatterns = [
    path('candidates', CandidateGP),
     path('candidates/<int:candidate_id>/', get_candidate_by_id, name='get_candidate_by_id'),
    path('candidate', UserView.as_view()),
    path('recruiters/<int:Id>', CandidateGPD),
    path('candidateCV/<int:candidateId>',getCVByCandidateId),
    path('candidates/recommended', get_recommended_candidates, name='get_recommended_candidates'),
    path('candidates/register',RegisterView.as_view()),
    path('candidate/login', LoginView.as_view()),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]