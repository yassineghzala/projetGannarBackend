from django.contrib import admin
from .models import JobOffer, Notification,Application,Match

# Register models separately
admin.site.register(JobOffer)
admin.site.register(Notification)
admin.site.register(Application)
admin.site.register(Match)
