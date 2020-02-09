from flask import Flask, request, Response, render_template
import paho.mqtt.client as mqtt
from pathlib import Path
import os
from configparser import ConfigParser
import json

app = Flask(__name__)

# Get configuration
current_dir = Path(os.path.abspath(os.path.dirname(__file__)))
settings_location = current_dir / '..' / 'config' / 'settings.ini'
config = ConfigParser()
config.read(settings_location)

# Setup MQTT
client = mqtt.Client()
client.connect(config['mqtt']['host'], int(config['mqtt']['port']), 60)
client.loop_start()


@app.route('/')
def hello_earth():
    return render_template('MainPage.html')


@app.route('/WMaskStudent')
def hello_world():
    return render_template('WMaskStudent.html')


@app.route('/WMaskStudent/Settings.html', methods=['POST'])
def hello_universe():
    print(request.form)
    return render_template('Settings.html', washer_id=request.form.get('washer_id'))


@app.route('/WMaskStudent/Settings/Timer.html')
def hello_galaxy():
    return render_template('Timer.html')


@app.route('/WMaskStudent/Settings/Timer/NotificationWasher.html')
def hello_milky_way():
    return render_template('NotificationWasher.html')


@app.route('/washer/user_interaction', methods=['POST'])
def handle_washer_interaction():
    """
    Handles when a user selects a washing machine to use. Below are the expected values and options.
    {
        "washer_id": int,
        "temp": (Cold, Warm, Hot),
        "soil_level": (Low, Medium, High),
        "spin_speed": (Low, Medium, High),
        "present_cycle": (Heavy Duty, Normal Eco, Delicate, Perm Press, Rinse and Spin, Spin)
    }
    """
    data = request.form
    print(data)
    mqtt_topic = 'washer/' + data.get('washer_id') + '/run_cycle'
    mqtt_message = {
        'temp': data.get('temp'),
        'soil_level': data.get('soil_level'),
        'spin_speed': data.get('spin_speed'),
        'present_cycle': data.get('present_cycle')
    }
    client.publish(mqtt_topic, json.dumps(mqtt_message))
    return render_template('Timer.html')


@app.route('/washer/run_command')
def washer_run_command():
    """
    Handle user making selections on what the washer should run. Expected in the format
    {

    }
    """
    client.publish('washer/8/run_cycle', 'temp data')
    return Response(status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
