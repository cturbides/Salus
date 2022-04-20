from asyncio import sleep
from .models import Sensores
import json
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

"""
class SendingSensorData(WebsocketConsumer):
    def start(self) -> None:
        self.accept()
        for _ in range(1000):
            time.sleep(2)
            try:
                sensors_data = Sensores.objects.all()
                if sensors_data:
                    sensors_data_list = list(sensors_data.values('roomTemperature', 'patientTemperature','roomHumidity','roomDustLevel',
                                                            'roomAirQuality','patientPulse'))
                else:
                    sensors_data_list = 'Te quiero mucho'
            except:
                sensors_data_list = 'Invalid result'
            self.send(text_data=json.dumps({"sensors_data":sensors_data_list}))
            
    def close(self, close_code) -> None:
        self.close()
        
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        room_id = text_data_json['roomId']
        try:
            sensors_data = Sensores.objects.filter(room_id=room_id)
            if sensors_data:
                sensors_data_list = list(sensors_data.values('roomTemperature', 'patientTemperature','roomHumidity','roomDustLevel',
                                                            'roomAirQuality','patientPulse'))
            else:
                sensors_data_list = 'Te quiero mucho'
        except:
            sensors_data_list = 'Invalid result'
        self.send(text_data=json.dumps({"sensors_data":sensors_data_list}))
"""

"""
We use can make not async functions and use the @sync_to_async
decorator to make them async contextualized. This will make possible
the function calling from an AsyncWebsocketConsumer.  
"""
@database_sync_to_async
def get_all_sensor_data():
    return list(Sensores.objects.all().values())

async def savingSensorData(data_list: list):
    for data in await get_all_sensor_data():
        data_list.append(data.values('roomTemperature', 'patientTemperature','roomHumidity','roomDustLevel',
                                                            'roomAirQuality','patientPulse')) if data else None

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
            sensors_data_list = await get_all_sensor_data()
            await self.send(text_data=json.dumps({"sensors_data":sensors_data_list}))
            await sleep(5)
            
    async def disconnect(self, code):
        await self.disconnect()