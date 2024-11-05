from django.urls import path

from Candidates.views import CandidateGP, CandidateGPD, RegisterView, ResumeGP
from JobOffers.views import JobOfferGP
from .views import MyTokenObtainPairView, UserView

from rest_framework_simplejwt.views import (

    TokenRefreshView,
)

urlpatterns = [
    path('candidates', CandidateGP),
    path('candidate', UserView.as_view()),
    path('recruiters/<int:Id>', CandidateGPD),
    path('resumes', ResumeGP),
    path('register',RegisterView.as_view()),
    path('token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]