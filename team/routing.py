from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/team/online/', consumers.OlineStatusConsumer.as_asgi())
]
