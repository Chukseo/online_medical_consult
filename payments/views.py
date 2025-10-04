# payments/views.py
import stripe
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from consultations.models import Consultation, Payment
from django.utils import timezone

def create_stripe_checkout(request, consultation_id):
    consultation = get_object_or_404(Consultation, pk=consultation_id, patient=request.user)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    amount = 500000  # 5000 NGN in kobo equivalent (use USD cents if USD)
    currency = "usd" if settings.STRIPE_PUBLIC_KEY else "ngn"

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        success_url=request.build_absolute_uri(reverse("payment_success")) + f"?cid={consultation.id}",
        cancel_url=request.build_absolute_uri(reverse("payment_cancel")) + f"?cid={consultation.id}",
        line_items=[{
            "price_data": {
                "currency": currency,
                "product_data": {"name": "Joyvor HC Video Consultation"},
                "unit_amount": amount,
            },
            "quantity": 1,
        }],
    )
    Payment.objects.update_or_create(
        consultation=consultation,
        defaults={"provider": "stripe", "amount": amount, "currency": currency, "external_id": session.id, "status": "initiated"}
    )
    return redirect(session.url)

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        external_id = session["id"]
        payment = Payment.objects.filter(provider="stripe", external_id=external_id).first()
        if payment:
            payment.status = "succeeded"
            payment.paid_at = timezone.now()
            payment.save()
            consultation = payment.consultation
            consultation.status = "scheduled"
            consultation.room_id = f"room-{consultation.id}-{int(timezone.now().timestamp())}"
            consultation.save()
    return HttpResponse(status=200)

# Paystackment Integration
import os
import requests

def init_paystack_payment(request, consultation_id):
    consultation = get_object_or_404(Consultation, pk=consultation_id, patient=request.user)
    amount = 500000  # in kobo
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "email": request.user.email or "patient@example.com",
        "amount": amount,
        "callback_url": request.build_absolute_uri(reverse("paystack_callback")) + f"?cid={consultation.id}",
    }
    r = requests.post("https://api.paystack.co/transaction/initialize", json=data, headers=headers)
    res = r.json()
    if res.get("status"):
        reference = res["data"]["reference"]
        Payment.objects.update_or_create(
            consultation=consultation,
            defaults={"provider": "paystack", "amount": amount, "currency": "NGN", "external_id": reference, "status": "initiated"}
        )
        return redirect(res["data"]["authorization_url"])
    return JsonResponse({"error": "Unable to initialize payment"}, status=400)

def paystack_callback(request):
    reference = request.GET.get("reference")
    cid = request.GET.get("cid")
    headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
    vr = requests.get(f"https://api.paystack.co/transaction/verify/{reference}", headers=headers)
    res = vr.json()
    payment = Payment.objects.filter(consultation_id=cid, external_id=reference, provider="paystack").first()
    if res.get("status") and res["data"]["status"] == "success" and payment:
        payment.status = "succeeded"
        payment.paid_at = timezone.now()
        payment.save()
        consultation = payment.consultation
        consultation.status = "scheduled"
        consultation.room_id = f"room-{consultation.id}-{int(timezone.now().timestamp())}"
        consultation.save()
        return redirect("join_room", room_id=consultation.room_id)
    return redirect("payment_cancel")