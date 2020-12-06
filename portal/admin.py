from django.contrib import admin
from .models import Jobs, AppliedJob, ShortList

admin.site.register(Jobs)
admin.site.register(AppliedJob)
admin.site.register(ShortList)
