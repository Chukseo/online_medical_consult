from django.db import models
from django.conf import settings

class Consultation(models.Model):
    STATUS_CHOICES = [
        ("pending_payment", "Pending Payment"),
        ("scheduled", "Scheduled"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="consultations")
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assigned_consultations", limit_choices_to={"is_doctor": True})
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default="pending_payment")
    room_id = models.CharField(max_length=64, blank=True)
    notes = models.TextField(blank=True)

class Payment(models.Model):
    PROVIDER_CHOICES = [("stripe", "Stripe"), ("paystack", "Paystack")]
    consultation = models.OneToOneField(Consultation, on_delete=models.CASCADE, related_name="payment")
    provider = models.CharField(max_length=16, choices=PROVIDER_CHOICES)
    amount = models.IntegerField(help_text="Amount in kobo/cent")
    currency = models.CharField(max_length=8, default="NGN")
    external_id = models.CharField(max_length=128, blank=True)  # charge/session/reference
    status = models.CharField(max_length=32, default="initiated")  # initiated, succeeded, failed
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

class CallSession(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.IntegerField(default=0)
    doctor_joined = models.BooleanField(default=False)
    patient_joined = models.BooleanField(default=False)