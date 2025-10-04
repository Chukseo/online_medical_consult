from django.urls import path
from .views import create_consultation, choose_payment, join_room

urlpatterns = [
    path("new/<int:doctor_id>/", create_consultation, name="create_consultation"),
    path("pay/<int:consultation_id>/", choose_payment, name="choose_payment"),
    path("room/<str:room_id>/", join_room, name="join_room"),
]