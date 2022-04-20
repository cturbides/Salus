from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/salusApp/room/<int:room_id>', consumers.ThrowingSensorData.as_asgi())
    ]