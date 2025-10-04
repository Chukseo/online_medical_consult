from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Consultation
from django.utils import timezone

@login_required
def create_consultation(request, doctor_id):
    consultation = Consultation.objects.create(patient=request.user, doctor_id=doctor_id)
    return redirect("choose_payment", consultation_id=consultation.id)

@login_required
def choose_payment(request, consultation_id):
    consultation = get_object_or_404(Consultation, pk=consultation_id, patient=request.user)
    return render(request, "consultations/choose_payment.html", {"consultation": consultation})

@login_required
def join_room(request, room_id):
    consultation = get_object_or_404(Consultation, room_id=room_id)
    if consultation.status not in ["scheduled", "in_progress"]:
        return redirect("patient_dashboard")
    consultation.status = "in_progress"
    consultation.save()
    role = "doctor" if request.user.is_doctor else "patient"
    return render(request, "consultations/room.html", {"room_id": room_id, "role": role, "consultation": consultation})

def payment_success(request):
    cid = request.GET.get("cid")
    c = Consultation.objects.filter(id=cid).first()
    return render(request, "payments/success.html", {"consultation": c})

def payment_cancel(request):
    return render(request, "payments/cancel.html")