#!/usr/bin/python3
""" Chess game """

from flask import Flask, render_template, request, jsonify, send_from_directory
import chess
import chess.svg
import chess.engine

app = Flask(__name__)

board = chess.Board()

@app.route('/')
def index():
    return render_template('index.html', board_svg=board_svg(board))

@app.route('/img/chesspieces/wikipedia/<filename>')
def do_nothing(filename):
    svgFile = filename.split('.')[0]
    return send_from_directory('img', f"{svgFile}.svg")

#@app.route('/img/<filename>')
#def get_image(filename):
#    return send_from_directory('img', filename)

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

def board_svg(board):
    return chess.svg.board(board=board)

if __name__ == '__main__':
    app.run(debug=True)
