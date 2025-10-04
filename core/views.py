
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from consultations.models import Payment, Consultation
from django.db.models import Sum
from django.utils import timezone

class LandingView(TemplateView):
    template_name = "core/landing.html"

@method_decorator(staff_member_required, name="dispatch")
class ReportsView(TemplateView):
    template_name = "core/reports.html"
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        qs = Payment.objects.filter(status="succeeded")
        ctx["total_revenue"] = qs.aggregate(Sum("amount"))["amount__sum"] or 0
        ctx["consultations_count"] = Consultation.objects.count()
        ctx["paid_consultations"] = Consultation.objects.filter(status__in=["scheduled","in_progress","completed"]).count()
        return ctx