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
        self.pawn_value = 30
        self.knight_value = 70
        self.bishop_value = 70
        self.rook_value = 100
        self.queen_value = 500
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
    
    def is_queen_safe(self, board, square):
        queen = board.piece_at(square)
        
        if queen is None or queen.piece_type != chess.QUEEN:
            return False # If not a queen, no function
        for attackers_square in board.attackers(not queen.color, square):
            if board.piece_at(attackers_square).piece_type != chess.KING:
                return False # Queen is attacked
        for defenders_square in board.attackers(queen.color, square):
            if board.piece_at(defenders_square).piece_type != chess.KING:
                return True # Queen is defended
        king_square = board.king(queen.color)
        if king_square and chess.square_distance(king_square, square) <= 1:
            return True # If queen close to her king, Queen happy
        return False # Defaults to undefended
    
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
                    if final_material_balance >= initial_material_balance:
                        return True
                else:
                    if final_material_balance <= initial_material_balance:
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
                        value += 20
                    elif i in almost_center_squares:
                        value += 8
                    value += self.get_piece_value(piece)
                    if bonus_score > 0:
                        value += 80
                elif piece.color == chess.BLACK:
                    bonus_score = -bonus_score
                    if i in center_squares:
                        value -= 20
                    elif i in almost_center_squares:
                        value -= 9
                    value += self.get_piece_value(piece)
                    if bonus_score < 0:
                        value -= 80
        return value
    
    def choose_move(self, board, colour_to_play):
        # Choose move function
        # Returns the best move
        best_move = None
        if colour_to_play is True:
            best_value = -float('inf')
        else:
            best_value = float('inf')
            
        early_game_threshold = 1 if colour_to_play is chess.WHITE else 2

        for move in board.legal_moves:
            #Check if the current position is a checkmate
                if board.fullmove_number <= early_game_threshold and ('q' in board.san(move) or "Q" in board.san(move)):
                # Skip queen moves in the early game
                    continue
                board.push(move)
                # IL VEUT TJR PAS VOIR LE MATE
                if board.is_checkmate() and board.turn == chess.WHITE:
                    print("checkmate noir")
                    best_move = move  # White wins
                    best_value = -1000000000
                    board.pop()
                    break
                elif board.is_checkmate() and board.turn == chess.BLACK:
                    print("checkmate blanc")
                    best_value = 1000000000
                    best_move = move  # Black wins
                    board.pop()
                    break
                score = self.minimax(board, 2, colour_to_play)
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
    
    def minimax(self, board, depth, maximizing_player, mate=0):
        if depth == 0 or board.is_game_over():
            return ia.evaluate_board(board)
        
        best_scoreb = float('inf')
        best_scorew = -float('inf')
        if maximizing_player:
            for move in board.legal_moves:
                temp_board = board.copy()
                temp_board.push(move)
                if ia.check_capture(board, move):
                    # Handle the capture move differently (by adding a bonus score)
                    current_score = self.evaluate_board(temp_board, 1000)
                else:
                    current_score = self.minimax(temp_board, depth - 1, chess.WHITE)
                if temp_board.piece_at(move.to_square).piece_type == chess.QUEEN:
                    if self.is_queen_safe(temp_board, move.to_square):
                        current_score += 40
                    else:
                        current_score -= 40  # Add a bonus score for moves that protect the queen
                if mate and board.turn == chess.WHITE:
                    current_score = 100000
                elif mate and board.turn == chess.BLACK:
                    current_score = -100000
                best_scorew = max(current_score, best_scorew)
        #print("best score for white = ", best_score)
            return best_scorew
        
        else:
            for move in board.legal_moves:
                temp_board = board.copy()
                temp_board.push(move)
                if ia.check_capture(board, move):
                    # Handle the capture move differently (by adding a bonus score)
                    current_score = self.evaluate_board(temp_board, 1000)
                else:
                    current_score = self.minimax(temp_board, depth - 1, chess.BLACK)
                if temp_board.piece_at(move.to_square).piece_type == chess.QUEEN:
                    if self.is_queen_safe(temp_board, move.to_square):
                        current_score -= 40
                    else:
                        current_score += 40   # Add a bonus score for moves that protect the queen
                if mate and board.turn == chess.WHITE:
                    current_score = 100000
                elif mate and board.turn == chess.BLACK:
                    current_score = -100000
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
board.push_san("e7e5")
board.push_san("f1c4")
board.push_san("a7a6")
board.push_san("d1f3")

ia = IA()
game_fens = []
try:
    with open("game_fens.json", "w") as f:
        for i in range(3):
            # Loop the game until it's over
            # user_move = ia.read_from_json(board)  # Get the move from JSON
            user_move = ia.choose_move(board, board.turn)
            print("white moved en dessous")
            board.push_san(str(user_move))  # Push the user's move
            game_fens.append(str((board.peek()))+ ": " + str(ia.evaluate_board(board)))
            print(board)
            if board.is_game_over():
                break
            move = ia.choose_move(board, board.turn)
            
            print("AI's move:", move)
            board.push(move)
            print("black moved en dessous")
            print(board)
            game_fens.append(str((board.peek()))+ ": " + str(ia.evaluate_board(board)))
            
        json.dump(game_fens,f)
    
    
except KeyboardInterrupt:
    pass
finally:
    ia.engine.quit()
