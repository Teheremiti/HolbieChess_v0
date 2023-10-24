#!/usr/bin/python3
""" Chess game """

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required,\
     logout_user
import chess
import chess.svg
import chess.engine
from models.user import User, login_manager

app = Flask(__name__)
login_manager.login_view = "login"
login_manager.init_app(app)

board = chess.Board()

@app.route('/', methods=['GET'])
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

@app.route('/login')
def login():
    # Implement your login logic here
    user = User("1")  # Replace with actual user information
    login_user(user)
    return "Logged in"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return "Logged out"

def board_svg(board):
    return chess.svg.board(board=board)

if __name__ == '__main__':
    app.run(debug=True)
