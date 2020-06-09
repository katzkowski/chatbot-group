from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
import json
import csv
import database_SQLite as database
from answerhandler_json import answerHandler

# from answerhandler_withdatabase import answerHandler

app = Flask(__name__, static_url_path='/static')

app.config["SECRET_KEY"] = "x!\x84Iy\xf9#gE\xedBQqg+\xf3A+\xe3\xd3\x01\x1a\xdf\xd2"

socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")


@app.route('/')
def send_index_page():
    return render_template('index.html')


@socketio.on('json')
def handleJson(payload):
    print("sending: " + payload)
    send(answerHandler(payload), json=True)


@socketio.on('user_registration')
def update_users(payload):
    readable_json = json.loads(payload)
    
    add_user_db_wop(readable_json['message'])

    initial_data = {"level": 0, "sender": "bot", "room": "elephant monument", "items": [], "mode": "game", "message": "Hello, " + readable_json['message'] + "!"}
    json_data = json.dumps(initial_data)
    send(json_data, json=True)
    intro_text = {"level": 0, "sender": "bot", "room": "elephant monument", "items": [], "mode": "game", "message": "current room"}
    json_data = json.dumps(intro_text)
    send(answerHandler(json_data), json=True)


@socketio.on('connect')
def connect():
    initial_data = {"level": 0, "sender": "bot", "room": "elephant monument", "items": [], "mode": "game", "message": "Welcome!"}
    json_data = json.dumps(initial_data)
    send(json_data, json=True)
    print("You are now connected with the server")


@socketio.on('disconnect')
def disconnect():
    print("You are disconneced from the server")


@socketio.on_error()
def error_handler(e):
    raise Exception("Some error happened, no further notice")

# Nutzer hinzufügen. Vorerst ohne Passwort
def add_user_db_wop(username):
    password = "123456"
    if isinstance(username, str) and not database.does_user_exist:
        database.insert_user(username, password)


if __name__ == "__main__":
    print("Try to start server...")
    socketio.run(app, host='0.0.0.0', debug=True)
