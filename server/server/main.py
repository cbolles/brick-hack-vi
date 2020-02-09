from flask import Flask, request, Response, render_template
import paho.mqtt.client as mqtt
from pathlib import Path
import os
from configparser import ConfigParser

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
def hello_world():
    return render_template('WMAskStudent.html')


@app.route('/Settings')
def hello_universe():
    return render_template('Settings.html')


@app.route('/washer/user_interaction', methods=['POST'])
def handle_washer_interaction():
    """
    Handles when a user interacts with a washing machine. Updates the status of the washing machine
    and the number of available washers. Expects information passed in like so.
    {
        "washer_id": int,
        "user_id": int,
        "washer_status": int,
        "time_remaining": long (time in seconds, -1 if not applicable)
    }
    """
    data = request.get_json()
    print(data['washer_id'])
    washer_id = data['washer_id']
    user_id = data['user_id']
    washer_status = data['washer_status']
    time_remaining = data['time_remaining']
    print('Washer: {}, By, {}, In state: {}, With {} remaining', washer_id, user_id, washer_status,
          time_remaining)
    return Response(status=200)


@app.route('/washer/run_command')
def washer_run_command():
    """
    Handle user making selections on what the washer should run. Expected in the format
    {
 
    }
    """
    print('here')
    print(client)
    client.publish('washer/8/run_cycle', 'temp data')
    return Response(status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
