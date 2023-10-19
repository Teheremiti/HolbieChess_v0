import chess
import chess.engine

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
    
    def square_trades(self, board, square):
        # Get all the pieces that are attacking a square
        trade = 0
        w_attackers = board.attackers(self.white, square)
        for attacker in w_attackers:
            piece_value = self.get_piece_value(board.piece_at(attacker))
            trade += piece_value if piece_value is not None else 0

        b_attackers = board.attackers(self.black, square)
        for attacker in b_attackers:
            piece_value = self.get_piece_value(board.piece_at(attacker))
            trade -= piece_value if piece_value is not None else 0

        return trade


                    
                    
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
                trade = self.square_trades(board, i)
                # Add value for white pieces and subtract for black pieces
                if piece.color == self.white:
                    if i in center_squares:
                        value += 20
                    elif i in almost_center_squares:
                        value += 10
                    value += self.get_piece_value(piece)
                else:
                    if i in center_squares:
                        value -= 20
                    elif i in almost_center_squares:
                        value -= 10
                    value -= self.get_piece_value(piece)
                    if self.square_trades(board, i) is True:
                        value += 30
                    else:
                        value -= 30
        return value
    
    def choose_move(self, board, colour_to_play):
        # Choose move function
        # Returns the best move
        best_move = None
        if colour_to_play == False:
            best_value = 9876
        else:
            best_value = -9876
        
        for move in board.legal_moves:
            # Create potential board
            board.push(move)
            # Evaluate the board
            board_value = self.evaluate_board(board)
            print (board_value)
            # Keep value while resetting the board to original state
            board.pop()
            if colour_to_play == False:
                if board_value < best_value:
                # If the move is better than the best move, it becomes the new best move
                    best_value = board_value
                    best_move = move
            if colour_to_play == True:
                if board_value > best_value:
                    # If the move is better than the best move, it becomes the new best move
                    best_value = board_value
                    best_move = move
        print("best move:", best_move)
        print("best value:", best_value)
        return best_move
        

def validity_check(board):
    while True:
        try:
            # Get human move (from command line for now) and checks for its validity
            # Also checks for wrong input
            usr_input = input("Enter your move: ")
            # Gets san value for input type
            san_move = usr_input
            # Turns it into uci for value check
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
    #while not board.is_game_over():
    for _ in range(15):
        # Loop the game until it's over
        user_move = validity_check(board)
        board.push_san(user_move)
        if board.is_game_over():
            break
        if board.turn == chess.WHITE:
            colour_to_play = chess.WHITE
        else:
            colour_to_play = False
        #move = ia.make_move(board)
        move = ia.choose_move(board, colour_to_play)
        board.push(move)
        eval = ia.evaluate_board(board)
        print (eval)
        print(board)
except KeyboardInterrupt:
    pass
finally:
    ia.engine.quit()
