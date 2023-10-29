#!/usr/bin/python3
""" Chess game """

from flask import Flask, render_template, request, jsonify, send_from_directory\
    , flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required,\
     logout_user, current_user
import chess
import chess.svg
import chess.engine

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20), nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)


# Chess and board related routes
board = chess.Board()

@app.route('/')
def index():
    return render_template('index.html', board_svg=board_svg(board))

@app.route('/img/chesspieces/wikipedia/<filename>', methods=['GET'])
def do_nothing(filename):
    svgFile = filename.split('.')[0]
    return send_from_directory('img', f"{svgFile}.svg")

@app.route('/move', methods=['POST'])
def move():
    global board
    move_uci = request.form['move']
    move = chess.Move.from_uci(move_uci)
    
    if move in board.legal_moves:
        board.push(move)
        return jsonify({'board_svg': board_svg(board), 'game_over': board.is_game_over()})
    else:
        return jsonify({'error': 'Invalid move'})

# User registration and login/logout routes
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    # Create the app context for the database
def create_app_context():
    return app.app_context()

with create_app_context():
    db.create_all()

@app.route('/img/logged_in')
@login_required
def logged_in():
    return send_from_directory('img', 'logged_in.png')
    
@app.route('/img/<filename>', methods=['GET'])
def image(filename):
    return send_from_directory('img', filename)

@app.route('/register', methods=['POST', 'GET'])
def register():
    firstName="guest"
    lastName="guest"
    username="guest"
    email="guest@guest.com"
    password="guest_pwd"
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

    if User.query.filter_by(username=username).first():
        flash('Username already taken', 'error')
    elif len(username) < 3:
        flash('Username must be 3 or more characters', 'error')
    else:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        newUser = User(firstName=firstName, lastName=lastName, username=username,
                       email=email, password=hashed_password)
        db.session.add(newUser)
        db.session.commit()
        flash('Welcome Holbie !', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Welcome back, Holbie !', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed, please check your credentials', 'error')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Succesfully logged out', 'success')
    return redirect(url_for('index'))


# AI move generation related routes
#@app.route('/get_ai_move', methods=['POST'])
#def get_ai_move():
#    data = request.get_json()
#    # Extract the move from data and pass it to your AI logic
#    # Generate the AI's move
#    ai_move = your_ai_logic(data['user_move'])
#    # Return the AI's move as JSON
#    return jsonify({'ai_move': ai_move})

#@app.route('/login')
#def login():
#    # Implement your login logic here
#    user = User("1")  # Replace with actual user information
#    login_user(user)
#    return "Logged in"

#@app.route('/logout')
#@login_required
#def logout():
#    logout_user()
#    return "Logged out"

# Create the chessboard
def board_svg(board):
    return chess.svg.board(board=board)
    

if __name__ == '__main__':
    app.run(debug=True)
