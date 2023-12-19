from django.contrib import admin
from.models import *


admin.site.register(CustomUser)
admin.site.register([Applicant])
admin.site.register(SavedModel)
admin.site.register([LoanApplicant])