from django.urls import re_path
from .consumers import SignalingConsumer

websocket_urlpatterns = [
    re_path(r"ws/consult/(?P<room_id>[\w-]+)/$", SignalingConsumer.as_asgi()),
]