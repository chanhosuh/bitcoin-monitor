from django.urls import path

from .consumers import BlockConsumer


websocket_urlpatterns = [
    path("ws/block", BlockConsumer),
]
