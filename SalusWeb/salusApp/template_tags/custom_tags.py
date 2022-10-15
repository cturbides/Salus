from django.template.defaulttags import register
from salusApp.models import Sensors

@register.filter
def is_here(dictionary: dict, key: str):
    return dictionary.get(key, False)

@register.simple_tag
def get_item(Sensor: Sensors, item: str):
    return getattr(Sensor, item)