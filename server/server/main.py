from flask import Flask, request, Response, render_template

app = Flask(__name__)

@app.route('/')
def hello_earth():
    return render_template('MainPage.html')


@app.route('/WMaskStudent')
def hello_world():
    return render_template('WMaskStudent.html')


@app.route('/WMaskStudent/Settings.html')
def hello_universe():
    return render_template('Settings.html')


@app.route('/WMaskStudent/Settings/Timer.html')
def hello_galaxy():
    return render_template('Timer.html')


@app.route('/WMaskStudent/Settings/Timer/NotificationWasher.html')
def hello_milky_way():
    return render_template('NotificationWasher.html')




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


if __name__ == '__main__':
    app.run(host='0.0.0.0')
