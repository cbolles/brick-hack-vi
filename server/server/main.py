from flask import Flask, request, render_template
import paho.mqtt.client as mqtt
from pathlib import Path
import os
from configparser import ConfigParser
import time
from database import WasherDatabase
import threading

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

washer_db = WasherDatabase(client)


@app.route('/')
def hello_earth():
    return render_template('MainPage.html')


@app.route('/WMaskStudent')
def hello_world():
    available_washers = washer_db.get_available_washers()
    if len(available_washers) == 0:
        return render_template('WMUnavailable.html')
    return render_template('WMaskStudent.html', available_washers=washer_db.get_available_washers())


@app.route('/WMaskStudent/Settings.html', methods=['POST'])
def hello_universe():
    return render_template('Settings.html', washer_id=request.form.get('washer_id'))


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
    # Create cycle data
    data = request.form
    cycle_data = {
        'temp': data.get('temp'),
        'soil_level': data.get('soil_level'),
        'spin_speed': data.get('spin_speed'),
        'present_cycle': data.get('present_cycle')
    }

    # Update washer
    washer_id = int(data.get('washer_id'))
    washer = washer_db.get_by_id(washer_id)
    washer.run_cycle(cycle_data)

    # Set timer
    finish_time = int(round(time.time() * 1000)) + 15000
    return render_template('Timer.html', finish_time=finish_time, washer_id=data.get('washer_id'))


@app.route('/washer/washer_complete/<washer_id>')
def washer_complete(washer_id):
    """
    Handles when the washing cycle is complete. Allows the user to unlock the door, starts a timer
    representing how long the user has to collect their laundry before the door is automatically
    unlocked.
    """
    # Update washer
    washer = washer_db.get_by_id(int(washer_id))
    washer.cycle_complete()

    finish_time = int(round(time.time() * 1000)) + 30000
    return render_template('NotificationWasher.html', washer_id=washer_id, finish_time=finish_time)


@app.route('/washer/unlock/<washer_id>')
def washer_unlock(washer_id):
    """
    Handles when the user has unlocked the washer completing their interaction with that washer
    """
    # Update washer
    washer = washer_db.get_by_id(int(washer_id))
    washer.unlock()

    return render_template('MainPage.html')


def support_thread():
    threading.Timer(3.0, support_thread).start()
    washer_db.check_timeouts()


if __name__ == '__main__':
    support_thread()
    app.run(host='0.0.0.0')
