from flask import Flask, request, Response

app = Flask(__name__)


@app.route('/hello')
def hello_world():
    return """
    <!DOCTYPE html>
<head>
   <title>RIT Laundry Services</title>
</head>
<body style="background-color:#ffd1b3;">
<body>  
    <h1>Welcome to RIT's Laundry Services</h1>
    <h2>No washing Machines are available at this time.</h2>
    <p>The next available washing machine will finish it's cycle in: 06:23 minutes</p>
    <img src="/static/washing machine.png" alt="Washing Machine"/>
    
    """


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
