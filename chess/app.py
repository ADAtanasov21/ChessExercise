from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

#储存注册数据 (in-memory for demo)
registrations = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/chess-board')
def chess_board():
    return render_template('board.html')

@app.route('/api/register', methods=['POST'])
def submit_registration():
    data = request.json
    registration = {
        'name': data.get('name'),
        'email': data.get('email'),
        'phone': data.get('phone'),
        'skill_level': data.get('skill_level'),
        'timestamp': datetime.now().isoformat()
    }
    registrations.append(registration)
    return jsonify({'success': True, 'message': 'Успешна регистрация!'})

@app.route('/api/registrations', methods=['GET'])
def get_registrations():
    return jsonify(registrations)

if __name__ == '__main__':
    app.run(debug=True)
