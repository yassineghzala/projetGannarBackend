from django.contrib import admin

from Candidates.models import Candidate, Resume

# Register your models here.
admin.site.register(Candidate)
admin.site.register(Resume)