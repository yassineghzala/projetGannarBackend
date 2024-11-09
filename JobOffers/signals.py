from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Application, Notification

@receiver(post_save, sender=Application)
def create_notification(sender, instance, created, **kwargs):
    if created:
        job_offer = instance.jobOffer
        candidate = instance.candidate
        recruiter = job_offer.recruiter  # Corrected: fetch recruiter from jobOffer

        content = f"{candidate.name} has applied for your job offer: {job_offer.name}"
        Notification.objects.create(
            content=content,
            recruiter=recruiter,
            job_offer=job_offer,
            candidate=candidate
        )
