from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

# When a user connects
@socketio.on('connect')
def handle_connect():
    print("User connected:", request.sid)
    emit('chat_message', {'user': 'System', 'msg': 'A new user has joined the chat!'}, broadcast=True)

# When a user disconnects
@socketio.on('disconnect')
def handle_disconnect():
    print("User disconnected:", request.sid)
    emit('chat_message', {'user': 'System', 'msg': 'A user has left the chat!'}, broadcast=True)

# Handle chat messages
@socketio.on('send_message')
def handle_message(data):
    user = data.get('user', 'Anonymous')
    msg = data.get('msg', '')
    emit('chat_message', {'user': user, 'msg': msg}, broadcast=True)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Chat app on http://localhost:{port}")
    socketio.run(app, host='0.0.0.0', port=port)