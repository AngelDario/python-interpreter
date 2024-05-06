from flask import Flask, jsonify, request
import subprocess
from flask_cors import CORS 
import platform
import socket

app = Flask(__name__)
CORS(app)

def get_machine_info():
    hostname = socket.gethostname()
    return {
        "hostname": platform.node(),
        "system": platform.system(),
        "ip": socket.gethostbyname(hostname),
        "release": platform.release()
    }

@app.route('/', methods=['POST'])
def processScript():
    data = request.get_json()
    code = data.get("code", "")
        
    # Ejecutar el código en un proceso separado
    subp = subprocess.Popen(['python3'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = subp.communicate(code.encode('utf-8'))
        
    # Capturar la salida y los errores en variables
    output_str = out.decode('utf-8')
    error_str = err.decode('utf-8')
    print(output_str);
    # Crear un diccionario para almacenar el resultado y los errores
    result_dict = {
        "result": output_str,
        "error": error_str,
        "machine_info": get_machine_info()
    }
    return jsonify(result_dict)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)