
import piece

class Player():

    def __init__(self, playerId, team, pieceList):
        self.id = playerId
        self.team = team
        self.pieces = pieceList
        
        for piece in pieceList: # get reference to players king
            if piece.getPieceId().endswith('king'):
                self.king = piece

        # if checked, valid moves are restricted to unchecking
        # a function should verify status at beginning of every
        # turn
        self.inCheck = False 

    def __str__(self):
        return f"ID: {self.id} Team: {self.team}"

    def getPlayerId(self):
        return self.id

    def getPieces(self):
        return self.pieces

    def kingStatus(self):
        if self.king.checked:
            self.inCheck = True
