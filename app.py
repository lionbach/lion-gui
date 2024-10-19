from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import webbrowser
import threading
import eventlet

# Inicializar Flask y SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='eventlet')

# Ruta principal para servir index.html
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para recibir el título por POST y enviarlo vía WebSocket
@app.route('/set-title', methods=['POST'])
def set_title():
    title = request.json.get('title', '')
    if title:
        #socketio.emit('update_title', {'title': title}, broadcast=True)
        socketio.emit('update_title', {'title': title})
        return jsonify({'status': 'success', 'message': 'Title updated'}), 200
    return jsonify({'status': 'error', 'message': 'No title provided'}), 400

# Función para abrir el navegador automáticamente
def open_browser():
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    # Abre el navegador en un hilo separado
    threading.Timer(1, open_browser).start()
    # Ejecuta el servidor en modo producción con eventlet
    socketio.run(app, host='0.0.0.0', port=5000)
