#!/usr/bin/python3
""" Game class """

import chess
from models.base_model import BaseModel


class Game(BaseModel):
    """ Defines the Game class, which keeps a record of every game.
    
    Attributes:
        white (str): id of the white player
        black (str): id of the black player
        moves (str): Moves executed in the current game in SAN
        board (chess.Board): Visual representation of the current state of the
        board
    """
    white = ""
    black = ""
    moves = ""
    captured = []
    board = chess.Board()
    
    def validMove(self, move):
        """
        Checks if a move is valid or not.

        Args:
            move (str): Move to play from the command line
        """
        if self.board.parse_san(move) in self.board.legal_moves:
            return True
        return False
            
    
    def play(self, move):
        """
        Plays the specified move on the board and updates the moves and board
        strings.

        Args:
            move (str): Move to play on the current board
        """
        if self.validMove(move) and not self.gameOver():
            self.board.push_san(move)
            #self.moves =                   # Représenter les moves du jeu en SAN
            #self.captured =                # Documenter les pièces capturées

        if self.gameOver():
            print("White or black won !") # Implémenter un moyen de savoir quel joueur a gagné
            return
        
        if self.gameDraw():
            print("Draw")
            return

    def gameOver(self):
        """
        Checks if the current game came to an end, by checkmate, stalemate,
        or insufficient material.
        """
        board = self.board
        end = board.is_checkmate()\
            or board.is_stalemate()\
            or board.is_insufficient_material()

        if end:
            return True
        return False
    
    def gameDraw(self):
        """
        Checks if a forced draw occurs in the current game. For simplicity,
        a draw occurs if the same move is repeted three times in a row or if the
        game exceeds 50 moves.
        """
        board = self.board
        draw = board.can_claim_threefold_repetition()\
            or board.can_claim_fifty_moves()

        if draw:
            return True
        return False
