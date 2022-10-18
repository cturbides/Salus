from django.urls import path
from salusApp import consumers

websocket_urlpatterns = [
    path('ws/salusApp/room/<str:room_uuid>', consumers.ThrowingSensorData.as_asgi())
]