import chess
import chess.engine
import chess.pgn
from flask import Flask, request, jsonify
import json
import random

#Add king safety X
#Add pawn structure
#Add pawn promotion
#Add castling
class IA:
    # init IA class
    def __init__(self):
        self.pawn = chess.PieceType(1)
        self.knight = chess.PieceType(2)
        self.bishop = chess.PieceType(3)
        self.rook = chess.PieceType(4) 
        self.queen = chess.PieceType(5)
        self.king = chess.PieceType(6)
        self.white = chess.WHITE
        self.black = chess.BLACK
        self.pawn_value = 30
        self.knight_value = 50
        self.bishop_value = 50
        self.rook_value = 90
        self.queen_value = 500
        self.king_value = 900
    
    def check_king_safety(self, board: chess.Board) -> int:
        #Checks for king safety
        king_square = board.king(board.turn)
        safety_score = 0

        if king_square is None:
            return safety_score  # King not found

        # Evaluate king safety
        enemy_attackers = len(board.attackers(not board.turn, king_square)) * 10
        pawn_cover = self.check_pawn_cover(board, king_square) * 2

        safety_score = enemy_attackers - pawn_cover

        return safety_score

    def check_pawn_cover(self, board: chess.Board, king_square: int) -> int:
        """
        Evaluate pawn cover for the king. A well-protected king will receive a higher score
        """
        pawn_cover_score = 0

        file, rank = chess.square_file(king_square), chess.square_rank(king_square)

        # Check if pawns are in front of and adjacent to the king
        for i in range(file - 1, file + 2):
            for j in range(rank - 1, rank + 2):
                if 0 <= i < 8 and 0 <= j < 8:
                    square = chess.square(i, j)
                    if board.piece_at(square) == chess.Piece(self.pawn, board.turn):
                        pawn_cover_score += 1
        #print("pawn cover score : ", pawn_cover_score)
        return pawn_cover_score
    
    def get_piece_value(self, piece: chess.Piece) -> int:
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
    
    def check_piece_development(self, board: chess.Board, square: int, color_to_play: bool) -> bool:
        starting_board = chess.Board()
        piece = board.piece_at(square)
        starting_piece = starting_board.piece_at(square)
        if piece is not None and starting_piece is not None:
            if color_to_play == chess.WHITE:
                if piece.piece_type != starting_piece.piece_type:
                    return True
            else:
                if piece.piece_type != starting_piece.piece_type:
                    return True
        return False
            
    def evaluate_castling(self, board: chess.Board) -> int:
        castling_score = 0

        if board.has_kingside_castling_rights(board.turn):
            castling_score += 200  # Encourage kingside castling
        if board.has_queenside_castling_rights(board.turn):
            castling_score += 200  # Encourage queenside castling

        return castling_score  
        
    def evaluate_pawn_structure(self, board: chess.Board) -> int:
        pawn_structure_score = 0

        isolated_pawn_penalty = -10  # Penalty for isolated pawns
        doubled_pawn_penalty = -5    # Penalty for doubled pawns
        pawn_chain_bonus = 10       # Bonus for pawn chains
        passed_pawn_bonus = 15      # Bonus for passed pawns

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.piece_type == chess.PAWN:
                file = chess.square_file(square)
                rank = chess.square_rank(square)

                # Check for isolated pawns
                isolated_pawn = (
                    not board.piece_at(chess.square(file - 1, rank - 1)) and
                    not board.piece_at(chess.square(file, rank - 1)) and
                    not board.piece_at(chess.square(file + 1, rank - 1))
                )
                if isolated_pawn:
                    pawn_structure_score += isolated_pawn_penalty

                # Check for doubled pawns
                doubled_pawn = (
                    board.piece_at(chess.square(file, rank - 1)) and
                    not board.piece_at(chess.square(file, rank - 2))
                )
                if doubled_pawn:
                    pawn_structure_score += doubled_pawn_penalty

                # Check for pawn chains
                pawn_chain = (
                    not board.piece_at(chess.square(file, rank - 1)) and
                    (
                        board.piece_at(chess.square(file - 1, rank - 1)) or
                        board.piece_at(chess.square(file + 1, rank - 1))
                    )
                )
                if pawn_chain:
                    pawn_structure_score += pawn_chain_bonus

                # Check for passed pawns
                passed_pawn = (
                    not board.attackers(not piece.color, square) and
                    not board.attackers(piece.color, square)
                )
                if passed_pawn:
                    pawn_structure_score += passed_pawn_bonus

        return pawn_structure_score
    
    def is_queen_safe(self, board: chess.Board, square: int) -> bool:
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
    
    def check_capture(self, board: chess.Board, move: chess.Move) -> int:   
        initial_material_balance = self.evaluate_board(board)
        if board.is_capture(move):
            from_piece = board.piece_at(move.from_square)
            to_piece = board.piece_at(move.to_square)
        
            if from_piece is not None and to_piece is not None:
                capturing_piece = self.get_piece_value(from_piece)
                captured_piece = self.get_piece_value(to_piece)
                if board.turn is chess.WHITE:
                    final_material_balance = initial_material_balance - captured_piece + capturing_piece
                    if final_material_balance >= initial_material_balance:
                        return final_material_balance
                if board.turn is chess.BLACK:
                    final_material_balance = initial_material_balance + captured_piece - capturing_piece
                    if final_material_balance <= initial_material_balance:
                        return final_material_balance

        return 0  # If the move is not a capture, return False
                        
    def evaluate_board(self, board: chess.Board) -> int:
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
        outer_squares = [
            chess.A1,
            chess.A2,
            chess.A3,
            chess.A4,
            chess.A5,
            chess.A6,
            chess.A7,
            chess.A8,
            chess.H1,
            chess.H2,
            chess.H3,
            chess.H4,
            chess.H5,
            chess.H6,
            chess.H7,
            chess.H8
        ]
            
            
        for i in range(64):
            # Scan through all squares on the board
            piece = board.piece_at(i)
            if piece != None:
                #king_safety_value = self.check_king_safety(board)
                #pawn_cover_value = self.check_pawn_cover(board, board.king(board.turn))
                #castling_value = self.evaluate_castling(board)
                #total_value = castling_value #+ castling_value #+ pawn_structure_value
                #print("king safety value for {} :{} ".format(king_safety_value, board.turn))
                #print("pawn cover value for {} :{} ".format(pawn_cover_value, board.turn))
                ##print("castling value for {} :{} ".format(castling_value, board.turn))
                #print("total value for {} :{} ".format(total_value, board.turn))
                # Add value for white pieces and subtract for black pieces
                if piece.color == chess.WHITE:
                    #value += total_value
                    if self.check_piece_development(board, i, chess.WHITE):
                        value += 9
                    if i in center_squares:
                        value += 20
                    elif i in almost_center_squares:
                        value += 10
                    elif i is chess.KNIGHT and i in outer_squares:
                        value -= 70
                    value += self.get_piece_value(piece)
                elif piece.color == chess.BLACK:
                    #value -= total_value
                    if self.check_piece_development(board, i, chess.BLACK):
                        value -= 9
                    if i in center_squares:
                        value -= 20
                    elif i in almost_center_squares:
                        value -= 10
                    elif i is chess.KNIGHT and i in outer_squares:
                        value += 70
                    value += self.get_piece_value(piece)
        return value
    
    def calculate_risk_score(self, board: chess.Board) -> int:
        risk_score = 0

        # Check king safety
        king_safety_score = self.check_king_safety(board)
        risk_score += king_safety_score

        # Evaluate pawn structure
        pawn_structure_score = self.evaluate_pawn_structure(board)
        risk_score += pawn_structure_score

        return risk_score
    
    def choose_move(self, board, depth: int, alpha: float, beta: float, maximizing_player: bool) -> chess.Move:
        # Choose move function
        # Returns the best move
        best_move = None
        risk_score = ia.calculate_risk_score(board)

        if maximizing_player:
            best_value = -float('inf')
        else:
            best_value = float('inf')

        for move in board.legal_moves:
            board.push(move)
            # Check for checkmate scenarios
            if board.is_checkmate() and maximizing_player:
                board.pop()
                return move  # Win for the maximizing player

            if board.is_checkmate() and not maximizing_player:
                board.pop()
                return move  # Win for the minimizing player

            current_score = self.minimax(board, depth, alpha, beta, not maximizing_player)
            board.pop()

            if maximizing_player:
                current_score -= risk_score
                if current_score >= best_value:
                    best_value = current_score
                    best_move = move
                alpha = max(alpha, best_value)
            else:
                current_score += risk_score
                if current_score <= best_value:
                    best_value = current_score
                    best_move = move
                beta = min(beta, best_value)

            if beta <= alpha:
                break
        #print("best move : ", best_move)
        #print("best value : ", best_value)
        return best_move
    
    def minimax(self, board: chess.Board, depth: int, alpha: float, beta: float, maximizing_player: bool) -> float:
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        if maximizing_player:
            best_score = -float('inf')
            for move in board.legal_moves:
                board.push(move)
                if board.piece_at(move.to_square).piece_type == chess.QUEEN:
                    if board.fullmove_number <= 5:
                        board.pop()
                        continue
                    if self.is_queen_safe(board, move.to_square):
                        current_score = self.evaluate_board(board) + 40
                    else:
                        current_score = self.evaluate_board(board) - 40
                else:
                    current_score = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                best_score = max(best_score, current_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = float('inf')
            for move in board.legal_moves:
                board.push(move)
                if board.piece_at(move.to_square).piece_type == chess.QUEEN:
                    if self.is_queen_safe(board, move.to_square):
                        current_score = self.evaluate_board(board) - 40
                    else:
                        current_score = self.evaluate_board(board) + 40
                else:
                    current_score = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                best_score = min(best_score, current_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score
    
    def return_ai_move(self, board_fen):
        board = chess.Board(board_fen)
        new_move = self.choose_move(board, depth, -float('inf'), float('inf'), board.turn)
        return str(board.san(new_move))

ia = IA()
game_fens = []
depth = 3
potential_moves = [
    "e2e4",
    "d2d4",
    "c2c4",
    "g1f3",
    "b1c3"
]
board = chess.Board()
#try:
#    with open("game_fens.json", "w") as f:
#        for _ in range(10): # Loop the game until it's over
#            #user_move = self.read_from_json()  # Get the move from JSON
#            #user_move = input("Enter your move: ")
#            if board.is_repetition(3) or board.is_stalemate() or board.is_insufficient_material() or board.is_fifty_moves():
#                print("Draw!")
#                break
#            if board.fullmove_number <= 1:
#               board.push_san(random.choice(potential_moves))
#            else:
#                user_move = ia.choose_move(board, depth, -float('inf'), float('inf'), board.turn)
#                board.push_san(str(user_move))  # Push the user's move
#            print("white moved en dessous")   
#            game_fens.append(str((board.peek()))+ ": " + str(ia.evaluate_board(board)))
#            print(board)
#            if board.is_game_over():
#                break
#            move = ia.choose_move(board, depth, -float('inf'), float('inf'), board.turn)
#            board.push(move)
#            print("black moved en dessous")
#            print(board)
#            game_fens.append(str((board.peek()))+ ": " + str(ia.evaluate_board(board)))
#            
#        json.dump(game_fens,f)
#   
#   
#except KeyboardInterrupt:
#    pass
#finally:
#    print("bien ouej")
