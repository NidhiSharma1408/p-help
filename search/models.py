from django.db import models
from userauth.models import UserProfile
from django.utils import timezone
# Create your models here.

class DonationRequest(models.Model):
    sender = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="request_sent")
    receiver = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="request_received")
    description = models.TextField(max_length=None,blank=True)
    time_sent = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    class Meta:
        ordering = ['-time_sent']
        unique_together = ('sender','receiver')

class DonationHistory(models.Model):
    donated_to = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="acception_history")
    donated_by = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="donation_history")
    donated_on = models.DateField(blank=False,null=True)
    class Meta:
        ordering = ['-donated_on']


