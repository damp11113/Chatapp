from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Simple account manager (in-memory storage for demonstration purposes)
accounts = {'user1': 'password1', 'user2': 'password2'}

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in accounts and accounts[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@socketio.on('message')
def handle_message(message):
    emit('message', {'username': session['username'], 'message': message}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, port=6845)
