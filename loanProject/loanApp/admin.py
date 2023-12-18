from django.contrib import admin
# Register your models here.
from.models import *


admin.site.register(CustomUser)
admin.site.register([Applicant])
admin.site.register(SavedModel)
admin.site.register([LoanApplicant])