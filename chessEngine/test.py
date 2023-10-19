import chess

board = chess.Board()

board.push_san("e4")

if board.turn == chess.WHITE:
     colour_to_play = chess.WHITE
else:
    colour_to_play = chess.BLACK

print (colour_to_play)