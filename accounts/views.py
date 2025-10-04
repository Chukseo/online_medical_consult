
from django.views.generic import TemplateView, FormView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django import forms
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ["username", "display_name", "phone", "is_doctor", "password"]

class LoginView(FormView):
    template_name = "accounts/login.html"
    form_class = LoginForm
    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
        if user:
            login(self.request, user)
            return redirect("doctor_dashboard" if user.is_doctor else "patient_dashboard")
        return self.form_invalid(form)

class LogoutView(TemplateView):
    def get(self, request):
        logout(request)
        return redirect("landing")

class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = RegisterForm
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        login(self.request, user)
        return redirect("doctor_dashboard" if user.is_doctor else "patient_dashboard")

class DoctorDashboardView(TemplateView):
    template_name = "accounts/doctor_dashboard.html"

class PatientDashboardView(TemplateView):
    template_name = "accounts/patient_dashboard.html"