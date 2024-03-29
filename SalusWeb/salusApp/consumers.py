from asyncio import sleep
from salusApp.models import Sensors, Room
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

"""
We use can make not async functions and use the @sync_to_async
decorator to make them async contextualized. This will make possible
the function calling from an AsyncWebsocketConsumer.  
"""
@database_sync_to_async
def get_all_sensor_data(room_uuid: str):
    room = Room.objects.get(uuid=room_uuid)
    return list(Sensors.objects.filter(room=room).values())

class ThrowingSensorData(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.groupname = 'Rooms'
        await self.channel_layer.group_add(
            self.groupname,
            self.channel_name
        )
        await self.accept()
        sensors_data_list = list()
        while True:
            sensors_data = await get_all_sensor_data(self.scope['url_route']['kwargs']['room_uuid'])
            await self.send(text_data=json.dumps({"sensors_data":sensors_data}))
            await sleep(1.5)
    
    async def disconnect(self, code):
        await self.disconnect()