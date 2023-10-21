import chess
import chess.engine
import json

stockfish_path = "/usr/games/stockfish"

class IA:
    # init IA class
    def __init__(self):
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        self.pawn = chess.PieceType(1)
        self.knight = chess.PieceType(2)
        self.bishop = chess.PieceType(3)
        self.rook = chess.PieceType(4) 
        self.queen = chess.PieceType(5)
        self.king = chess.PieceType(6)
        self.white = chess.WHITE
        self.black = chess.BLACK
        self.pawn_value = 10
        self.knight_value = 30
        self.bishop_value = 30
        self.rook_value = 50
        self.queen_value = 90
        self.king_value = 900

    def make_move(self, board):
        # Move choosing function
        result = self.engine.play(board, chess.engine.Limit(time=0.1))
        move = result.move
        return move
    
    def get_piece_value(self, piece):
    # Assign values to piece objects
        piece_values = {
            self.pawn: self.pawn_value,
            self.knight: self.knight_value,
            self.bishop: self.bishop_value,
            self.rook: self.rook_value,
            self.queen: self.queen_value,
            self.king: self.king_value,
        }
        
        # Assign proper values to pieces
        piece_value = piece_values.get(piece.piece_type, 0)

        # Turn the value negative for black
        if piece.color == self.black:
            piece_value = -piece_value

        return piece_value
    
    #def check_piece_development(self, board, square):
    #    value = 0
    #   piece_at_square = board.piece_at(square)
    #    if piece_at_square is not None:
    #        if piece_at_square.moved:
    #            if piece_at_square.piece_type == chess.PAWN:
    #                value = 5
    #            else:
    #                value = 10
    #    return value
    
 #   def square_trades(self, board, square):
 #   # Get all the pieces that are attacking a square
 #       trade = 0
 #       w_attackers = board.attackers(chess.WHITE, square)
 #       for attacker in w_attackers:
 #           piece_value = self.get_piece_value(board.piece_at(attacker))
 #           if piece_value is not None:
 #               trade += piece_value
#
 #       b_attackers = board.attackers(chess.BLACK, square)
 #       for attacker in b_attackers:
 #           piece_value = self.get_piece_value(board.piece_at(attacker))
 #           if piece_value is not None:
 #               trade -= piece_value
#
 #       if trade > 0:
 #           return True
 #       else:
 #           return False
                    
    def evaluate_board(self, board):
        # Evaluate board function
        # Returns the board value
        value = 0
        center_squares = [
            chess.E4,
            chess.D4,
            chess.E5,
            chess.D5
        ]
        almost_center_squares = [
            chess.C3,
            chess.C4,
            chess.C5,
            chess.C6,
            chess.D3,
            chess.D6,
            chess.E3,
            chess.E6,
            chess.F3,
            chess.F4,
            chess.F5,
            chess.F6
        ]
        for i in range(64):
            # Scan through all squares on the board
            piece = board.piece_at(i)
            if piece != None:
                # Add value for white pieces and subtract for black pieces
                if piece.color == self.white:
                    if i in center_squares:
                        value += 10
                    elif i in almost_center_squares:
                        value += 5
                    value += self.get_piece_value(piece)
                    #if self.square_trades(board, i) is True:
                    #    value = 100
                    #elif self.square_trades(board, i) is False:
                    #    value = -10000
                elif piece.color == self.black:
                    if i in center_squares:
                        value -= 10
                    elif i in almost_center_squares:
                        value -= 5
                    value -= self.get_piece_value(piece)
                    #if self.square_trades(board, i) is True:
                    #    value = -100
                    #elif self.square_trades(board, i) is False:
                    #    value = +10000
                    #if self.square_trades(board, i) is True:
                    #    value += 30
                    #else:
                    #    value -= 30
        
        return value
    
    def choose_move(self, board, colour_to_play):
        # Choose move function
        # Returns the best move
        best_move = None
        if colour_to_play is True:
            best_value = -float('inf')
        else:
            best_value = float('inf')

        for move in board.legal_moves:
            board.push(move)
            score = self.minimax(board, 1, colour_to_play)
            board.pop()
            if colour_to_play == chess.WHITE:
                if score > best_value:
                    best_value = score
                    best_move = move
            elif colour_to_play == chess.BLACK:
                if score < best_value:
                    best_value = score
                    best_move = move
        print ("best move is:", best_move)
        print("and its score is :", best_value)
        return best_move
    
    def minimax(self, board, depth, maximizing_player):
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)
        if maximizing_player:
            best_score = -float('inf')
            for move in board.legal_moves:
                board.push(move)
                current_score = self.minimax(board, depth - 1, False)  # Switch to the opponent's turn
                board.pop()
                best_score = max(current_score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for move in board.legal_moves:
                board.push(move)
                current_score = self.minimax(board, depth - 1, True)  # Switch back to the player's turn
                board.pop()
                best_score = min(current_score, best_score)
            return best_score

            
    def read_from_json(self, board):
        json_file_path = "last_move.json"
        with open(json_file_path, "r") as json_file_r:
            last_move_data = json.load(json_file_r)
        last_move = last_move_data["last_move"]
        print(f"Last move played: {last_move} has been read from {json_file_path}.")
        return last_move

    
    def save_to_json(self, move):
        json_file_path = "last_move.json"
        last_move_data = {
            "last_move": move.uci()
        }
        with open(json_file_path, "w") as json_file_w:
            json.dump(last_move_data, json_file_w)
        print(f"Last move played: {move.uci()} has been saved to {json_file_path}.")
        
        

def validity_check(board):
    while True:
        try:
            # Get human move (from command line for now) and checks for its validity
            # Also checks for wrong input:
            usr_input = ia.read_from_json(board)
            # Gets san value for input type
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
    for _ in range(5):
        # Loop the game until it's over
        #user_move = ia.read_from_json(board)  # Get the move from JSON
        if board.fen() == chess.STARTING_FEN:
            user_move = "e2e4"
        else:
            user_move = ia.choose_move(board, board.turn)
        board.push_san(str(user_move))  # Push the user's move
        if board.is_game_over():
            break
        if board.turn == chess.WHITE:
            colour_to_play = chess.WHITE
        else:
            colour_to_play = chess.BLACK
        move = ia.choose_move(board, colour_to_play)
        print("AI's move:", move)
        board.push(move)
        print(board)
except KeyboardInterrupt:
    pass
finally:
    ia.engine.quit()
