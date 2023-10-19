import chess
import chess.engine

stockfish_path = "/usr/games/stockfish"

class IA:
    # init IA class
    def __init__(self):
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

    def make_move(self, board):
        # Move choosing function
        result = self.engine.play(board, chess.engine.Limit(time=0.1))
        move = result.move
        return move  

def validity_check(board):
    while True:
        try:
            # Get human move (from command line for now) and checks for its validity
            # Also checks for wrong input
            usr_input = input("Enter your move: ")
            san_move = usr_input
            uci_move = board.parse_san(san_move)
            if uci_move in board.legal_moves:
                return usr_input
            else:
                print("Illegal move, try again")
        except chess.IllegalMoveError:
            print("Illegal move, please try again")
        except ValueError:
            print("caps sensitive input, usage: $ e4d5")

board = chess.Board()
ia = IA()

try:
    while not board.is_game_over():
        # Loop the game until it's over
        user_move = validity_check(board)
        board.push_san(user_move)
        print(board)
        if board.is_game_over():
            break
        move = ia.make_move(board)
        board.push(move)
        print(board)
except KeyboardInterrupt:
    pass
finally:
    ia.engine.quit()
