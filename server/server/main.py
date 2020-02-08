from flask import Flask
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


@app.route('/washer/new_wash_cycle')
def handle_new_wash_cycle():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0')
