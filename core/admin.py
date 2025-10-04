
from django.contrib import admin
from consultations.models import Consultation, Payment, CallSession
from accounts.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "display_name", "is_doctor", "email")

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "doctor", "status", "created_at", "scheduled_at")
    list_filter = ("status", "created_at", "doctor")

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("consultation", "provider", "amount", "currency", "status", "paid_at")
    list_filter = ("provider", "status", "currency")