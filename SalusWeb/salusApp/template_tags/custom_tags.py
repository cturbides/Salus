from django.template.defaulttags import register
from salusApp.models import Sensors

@register.filter
def is_here(dictionary: dict, key: str):
    return dictionary.get(key, False)

@register.simple_tag
def get_item(Sensor: Sensors, item: str):
    return getattr(Sensor, item)

@register.simple_tag
def muscle_state_class(Sensor: Sensors, item: str):
    muscle_state = int(getattr(Sensor, item))
    message = "status "
    
    if muscle_state < 30:
        message += "completed"
    elif muscle_state < 60:
        message += "process"
    else:
        message += "pending"
    
    return message
        
@register.simple_tag
def muscle_state_message(Sensor: Sensors, item: str):
    muscle_state = int(getattr(Sensor, item))
    message = str()
    
    if muscle_state < 30:
        message = "Relajado"
    elif muscle_state < 60:
        message = "Tensos"
    else:
        message = "Rígido"
    
    return message