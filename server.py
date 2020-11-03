import can
import cantools
import json

db = cantools.database.load_file('dbc/Megasquirt_CAN_Modified.dbc', encoding='utf-8')
data = {}

def read_can():
    global data

    bus = can.interface.Bus('vcan0', bustype='socketcan')
    for message in bus:
        try:
            decoded = db.decode_message(message.arbitration_id, message.data)
            data.update(decoded)
            socketio.emit('data_broadcast', json.dumps(data))
            print(str(decoded))
        except:
            print("Unable to decode message!")
        finally:
            print(str(message))

from flask import Flask, render_template
from flask_socketio import SocketIO

import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change this'
socketio = SocketIO(app)
socketio.start_background_task(target=read_can)

@app.route('/')
def index():
    return render_template('index.html', db=db)
