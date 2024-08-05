from django.urls import path
from .consumers import NotificationConsumer

websocket_urlpatterns = [
    path('ws/wsc/', NotificationConsumer.as_asgi()),
]
