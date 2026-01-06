from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-chess-2026'

# Список со регистрирани корисници
registrations = []
logged_in_user = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/chess-board')
def chess_board():
    return render_template('board.html')

@app.route('/login')
def login():
    if 'user_email' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    # Find user by email
    user = None
    for reg in registrations:
        if reg['email'] == session['user_email']:
            user = reg
            break
    
    return render_template('dashboard.html', user=user, all_users=registrations)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/api/register', methods=['POST'])
def submit_registration():
    data = request.json
    
    # Check if user already exists
    for reg in registrations:
        if reg['email'] == data.get('email'):
            return jsonify({'success': False, 'message': 'Този имейл вече е регистриран!'})
    
    registration = {
        'firstName': data.get('firstName'),
        'lastName': data.get('lastName'),
        'email': data.get('email'),
        'phone': data.get('phone'),
        'gender': data.get('gender'),
        'additionalInfo': data.get('additionalInfo'),
        'registeredAt': datetime.now().isoformat()
    }
    registrations.append(registration)
    return jsonify({'success': True, 'message': 'Успешна регистрација!'})

@app.route('/api/login', methods=['POST'])
def submit_login():
    data = request.json
    email = data.get('email')
    
    # Check if user exists
    user = None
    for reg in registrations:
        if reg['email'] == email:
            user = reg
            break
    
    if user:
        session['user_email'] = email
        return jsonify({'success': True, 'message': 'Успешен вход!'})
    else:
        return jsonify({'success': False, 'message': 'Потребителят не е намерен!'})

@app.route('/api/registrations', methods=['GET'])
def get_registrations():
    return jsonify(registrations)

if __name__ == '__main__':
    app.run(debug=True)
