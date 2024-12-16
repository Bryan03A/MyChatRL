from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app)

users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Logged in user')

@socketio.on('join')
def handle_join(username):
    users[request.sid] = username  
    print(f'{username} has joined the chat')
    join_room('chat')  
    send(f'{username} has joined the chat', room='chat')  

@socketio.on('message')
def handle_message(msg):
    username = users.get(request.sid, 'Anónimo')
    print(f'Message received from {username}: {msg}')
    send(f'{username}: {msg}', room='chat')  

@socketio.on('disconnect')
def handle_disconnect():
    username = users.get(request.sid, 'Anónimo')
    print(f'{username} has been disconnected')
    send(f'{username} has been disconnected', room='chat')
    leave_room('chat')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)
