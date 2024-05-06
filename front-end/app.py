from flask import Flask, render_template, request
from flask_cors import CORS  # Importa la extensión Flask-CORS
import os
import socket
from flask import Flask, render_template
from flask_socketio import SocketIO, emit


# Obtener el nombre del host (hostname)
hostname = socket.gethostname()

# Obtener la dirección IP del host
ip_address = socket.gethostbyname(hostname)

app = Flask(__name__)
CORS(app)  # Habilita CORS en tu aplicación
socketio = SocketIO(app)

@app.route('/')
def index():
    # Obtener la dirección IP del host
    host_ip = request.remote_addr

    # Otros datos del servidor (puedes agregar más según tus necesidades)
    server_info = {
        'hostname': hostname,
        'direccion_ip': ip_address,
        'puerto': 5000,  # Puerto en el que se ejecuta la aplicación Flask
        'version': '1.0'
    }

    return render_template('index.html', host_ip=host_ip, server_info=server_info)

@socketio.on('text_update')
def handle_text_update(data):
    emit('text_update', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug=True, allow_unsafe_werkzeug=True)