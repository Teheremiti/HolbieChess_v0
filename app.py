#!/usr/bin/python3
""" Chess game """

from flask import Flask, render_template, request, jsonify, send_from_directory
from ia import IA

app = Flask(__name__)


# Basic routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<page>.html')
def loadpage(page):
    return render_template(f'{page}.html')

@app.route('/img/<filename>', methods=['GET'])
def image(filename):
    return send_from_directory('img', filename)

@app.route('/gif/<filename>', methods=['GET'])
def gif(filename):
    return send_from_directory('gif', filename)

# AI move generation
ia = IA()
@app.route('/IAMove', methods=['POST'])
def receive_move():
    # Get the JSON data sent from JavaScript
    game_fen = request.json
    
    # Get a move from the IA
    ai_response = ia.return_ai_move(game_fen)

    # Return a JSON response to JavaScript
    return jsonify(ai_response)


if __name__ == '__main__':
    app.run(debug=True)
