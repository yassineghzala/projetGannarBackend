from django.urls import path, include

from Recruiters.views import LoginView, RecruiterGPD, RecruiterGP, deleteNotification, notifyRecruiter
urlpatterns = [
    path('recruiters', RecruiterGP),
    path('recruiters/<int:Id>', RecruiterGPD),
    path('notifications/<int:recruiterId>/jobOffer/<int:jobOfferId>/candidate/<int:candidateId>', notifyRecruiter),
    path('notifications/<int:notificationId>', deleteNotification),
    path('recruiter-token', LoginView.as_view()),
]