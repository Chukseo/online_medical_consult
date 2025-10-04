from django.urls import path
from .views import create_stripe_checkout, stripe_webhook, init_paystack_payment, paystack_callback
from consultations.views import payment_success, payment_cancel

urlpatterns = [
    path("stripe/<int:consultation_id>/", create_stripe_checkout, name="stripe_checkout"),
    path("stripe/webhook/", stripe_webhook, name="stripe_webhook"),
    path("paystack/<int:consultation_id>/", init_paystack_payment, name="paystack_init"),
    path("paystack/callback/", paystack_callback, name="paystack_callback"),
    path("success/", payment_success, name="payment_success"),
    path("cancel/", payment_cancel, name="payment_cancel"),
]