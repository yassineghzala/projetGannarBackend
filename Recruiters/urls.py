from django.urls import path, include

from Recruiters.views import RegisterView
from Recruiters.views import LoginView, RecruiterGPD, RecruiterGP
urlpatterns = [
    path('recruiters', RecruiterGP),
    path('recruiters/<int:Id>', RecruiterGPD),
    # path('notifications/<int:recruiterId>/jobOffer/<int:jobOfferId>/candidate/<int:candidateId>', notifyRecruiter),
    # path('notifications/<int:notificationId>', deleteNotification),
    path('recruiters/register',RegisterView.as_view()),
    path('recruiter/login', LoginView.as_view()),
]