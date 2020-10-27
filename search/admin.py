from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.DonationRequest)
admin.site.register(models.DonationHistory)