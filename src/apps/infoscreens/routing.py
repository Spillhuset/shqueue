# chat/routing.py
from django.urls import path

from . import consumers

websocket_urlpatterns = [
  path("ws/infoscreens/queues/<int:queue_id>", consumers.InfoscreenConsumer.as_asgi()),
]
