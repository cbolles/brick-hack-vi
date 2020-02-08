from flask import Flask
app = Flask(__name__)


@app.route('/hello')
def hello_world():
    return 'Hello, World!'


@app.route('/washer/new_wash_cycle')
def handle_new_wash_cycle():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0')
