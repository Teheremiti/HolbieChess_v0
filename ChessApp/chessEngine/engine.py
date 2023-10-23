import chess
import chess.engine
import json
import chess.pgn

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
        if piece.color == chess.BLACK:
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
    def check_capture(self, board, move):
        initial_material_balance = self.evaluate_board(board)
        if board.is_capture(move):
            from_piece = board.piece_at(move.from_square)
            to_piece = board.piece_at(move.to_square)
        
            if from_piece is not None and to_piece is not None:
                capturing_piece = self.get_piece_value(from_piece)
                captured_piece = self.get_piece_value(to_piece)
                if board.turn is chess.WHITE:
                    final_material_balance = initial_material_balance - captured_piece + capturing_piece
                elif board.turn is chess.BLACK:
                    final_material_balance = initial_material_balance + captured_piece - capturing_piece
                if board.turn is chess.WHITE:
                    #print("BLACK ca rentre dans le true du check capture")
                    if final_material_balance <= initial_material_balance:
                        return True
                else:
                    #print("WHITE")
                    if final_material_balance >= initial_material_balance:
                        return True

        return False  # If the move is not a capture, return False
                        
    def evaluate_board(self, board, bonus_score=0):
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
                if piece.color == chess.WHITE:
                    if i in center_squares:
                        value += 5
                    elif i in almost_center_squares:
                        value += 2
                    value += self.get_piece_value(piece)
                    #print(bonus_score) if bonus_score > 0 else None
                    if bonus_score > 0:
                        value += 50
                    #if self.square_trades(board, i) is True:
                    #    value = 100
                    #elif self.square_trades(board, i) is False:
                    #    value = -10000
                    #print("white value = ", value)
                elif piece.color == chess.BLACK:
                    bonus_score = -bonus_score
                    if i in center_squares:
                        value -= 5
                    elif i in almost_center_squares:
                        value -= 2
                    value += self.get_piece_value(piece)
                    if bonus_score < 0:
                        value -= 50
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
            if colour_to_play is chess.WHITE:
                if score > best_value:
                    best_value = score
                    best_move = move
            elif colour_to_play is chess.BLACK:
                if score < best_value:
                    best_value = score
                    best_move = move
        print(best_move)
        print(best_value)
        return best_move
    
    def minimax(self, board, depth, maximizing_player):
        if depth == 0 or board.is_game_over():
            return ia.evaluate_board(board)
        
        best_scoreb = float('inf')
        best_scorew = -float('inf')
        if maximizing_player:
            for move in board.legal_moves:
                temp_board = board.copy()
                temp_board.push(move)
        #print(ia.check_capture(board, move))
        #print(ia.check_capture(board, move))
                if ia.check_capture(board, move):
                    # Handle the capture move differently (by adding a bonus score)
                    current_score = self.evaluate_board(board, 1000)
                else:
                    current_score = self.minimax(board, depth - 1, chess.WHITE)
                best_scorew = max(current_score, best_scorew)
        #print("best score for white = ", best_score)
            return best_scorew
        else:
            for move in board.legal_moves:
                temp_board = board.copy()
                temp_board.push(move)
                #print(ia.check_capture(board, move))
                if ia.check_capture(board, move):
                    # Handle the capture move differently (by adding a bonus score)
                    current_score = self.evaluate_board(board, 1000)
                else:
                    current_score = self.minimax(board, depth - 1, chess.BLACK)
                    #print("current score for black = ", current_score)
                best_scoreb = min(current_score, best_scoreb)
                #print("best score final for black = ", best_scoreb)
                #print("best score for black = ", best_score)
               
            return best_scoreb
         
    def read_from_json(self):
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
board.push_san("e2e4")
board.push_san("d7d5")
board.push_san("b1c3")

ia = IA()
game_fens = []
try:
    with open("game_fens.json", "w") as f:
        for _ in range(2):
            # Loop the game until it's over
            # user_move = ia.read_from_json(board)  # Get the move from JSON
            
            user_move = ia.choose_move(board, board.turn)
            print("white moved en dessous")
            board.push_san(str(user_move))  # Push the user's move
            game_fens.append(str((board.peek())))
            print(board)
            if board.is_game_over():
                break
            move = ia.choose_move(board, board.turn)
            
            print("AI's move:", move)
            board.push(move)
            print("black moved en dessous")
            print(board)
            game_fens.append(str((board.peek())))
            
        json.dump(game_fens,f)
    
    
except KeyboardInterrupt:
    pass
finally:
    ia.engine.quit()
