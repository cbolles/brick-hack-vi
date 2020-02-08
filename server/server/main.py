from flask import Flask, request, Response

app = Flask(__name__)


@app.route('/')
def hello_world():
    return """
    <!DOCTYPE html>
<html lang="en">
<head>
    <title>RIT Laundring Services</title>
</head>
<body style="background-color:#ffd1b3;">
    <h1>Washing Machines </h1>
    <img src="/static/OpenWM.png" alt="Washing Machine"/>
    <form action="/action_page.php" target="_blank" method="GET">
        <fieldset>
            <legend>Available washing machines are:</legend>
            <input type="radio" name="number" value="machine1" > Washing Machine 1<br>
            <input type="radio" name="number" value="machine2" > Washing Machine 2<br>
            <input type="radio" name="number" value="machine3" > Washing Machine 3<br>
            <input type="radio" name="number" value="machine4" > Washing Machine 4<br>
            <input type="submit" value="Submit">
        </fieldset>
    </form>
</body>
</html>
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
