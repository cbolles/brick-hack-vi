from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return """
    <head>
        <title>RIT Laundring Services</title>
    </head>
    <body style="background-color:#ffd1b3;">  
        <h1>Available Washing Machines are: </h1>
        
        <form action="/action_page.php" target="_blank" method="GET">
            <fieldset>
                <legend>Here:</legend>
                <input type="radio" name="number" value="machine1" > Washing Machine 1<br>
                <input type="radio" name="number" value="machine2" > Washing Machine 2<br>
                <input type="radio" name="number" value="machine3" > Washing Machine 3<br>
                <input type="radio" name="number" value="machine4" > Washing Machine 4<br>
                <input type="submit" value="Submit">
            </fieldset>
        </form>
    </body>
    """


if __name__ == '__main__':
    app.run(host='0.0.0.0')
