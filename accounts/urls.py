from django.urls import path
from .views import LoginView, LogoutView, DoctorDashboardView, PatientDashboardView, RegisterView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("doctor/", DoctorDashboardView.as_view(), name="doctor_dashboard"),
    path("patient/", PatientDashboardView.as_view(), name="patient_dashboard"),
]