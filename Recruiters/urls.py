from django.urls import path, include

from Recruiters.views import RecruiterGPD, RecruiterGP
urlpatterns = [
    path('recruiters', RecruiterGP),
    path('recruiters/<int:Id>', RecruiterGPD)
    
]