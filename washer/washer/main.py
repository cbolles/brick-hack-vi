from gpiozero import Button, LED
import requests
from signal import pause
from pathlib import Path
import os
from configparser import ConfigParser
import paho.mqtt.client as mqtt
import time


LOCK_BUTTON_GPIO = 4
AVAILABLE_LED_GPIO = 17
UNAVAILABLE_LED_GPIO = 27


lock_button = Button(LOCK_BUTTON_GPIO)
available_led = LED(AVAILABLE_LED_GPIO)
unavailable_led = LED(UNAVAILABLE_LED_GPIO)
is_available = True


def toggle():
    global is_available
    is_available = not is_available
    if is_available:
        available_led.on()
        unavailable_led.off()
    else:
        available_led.off()
        unavailable_led.on()


def handle_mqtt_connection(client, userdata, flags, rc):
    client.subscribe('washer/8/run_cycle')

def handle_mqtt_message(client, userdata, msg):
    print('here')

def main():
    # Get configuration settings
    current_dir = Path(os.path.abspath(os.path.dirname(__file__)))
    settings_file = current_dir / '..' / 'config' / 'settings.ini'
    config = ConfigParser()
    config.read(settings_file)

    # Establish connection to MQTT
    mqtt_client = mqtt.Client()
    mqtt_client.on_messsage = handle_mqtt_message
    mqtt_client.connect('129.21.65.60')
    topic = 'washer/' + config['instance']['washer_id'] + '/run_cycle'
    print(topic)
    mqtt_client.subscribe('washer/8/run_cycle')
    mqtt_client.loop_forever()


if __name__ == '__main__':
    main()
