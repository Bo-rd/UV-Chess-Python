
from pieceSub import *
import handler as HANDLER

class Player():

    def __init__(self, playerId, team, start, SCREEN):
        print("In init")
        self.id = playerId
        self.team = team # team needs to be capitalized for graphic path

        # if checked, valid moves are restricted to unchecking
        self.inCheck = False

        path = "./graphics/pieces/" + team.lower() + "/"

        board = HANDLER.getTiles()

        r1 = Rook(start[0][0], start[0][1], self.team, path + "rook" + self.team + ".png",
                  pieceId=self.team + " rook", surface=SCREEN)
        board[start[0][1]][start[0][0]].putPiece(r1)

        k1 = Knight(start[1][0], start[1][1], self.team, path + "knight" + self.team + ".png",
                  pieceId=self.team + " knight", surface=SCREEN)
        board[start[1][1]][start[1][0]].putPiece(k1)

        b1 = Bishop(start[2][0], start[2][1], self.team, path + "bishop" + self.team + ".png",
                  pieceId=self.team + " bishop", surface=SCREEN)
        board[start[2][1]][start[2][0]].putPiece(b1)

        queen = Queen(start[3][0], start[3][1], self.team, path + "queen" + self.team + ".png",
                  pieceId=self.team + " queen", surface=SCREEN)
        board[start[3][1]][start[3][0]].putPiece(queen)

        king = King(start[4][0], start[4][1], self.team, path + "king" + self.team + ".png",
                  pieceId=self.team + " king", surface=SCREEN)
        board[start[4][1]][start[4][0]].putPiece(king)

        b2 = Bishop(start[5][0], start[5][1], self.team, path + "bishop" + self.team + ".png",
                  pieceId=self.team + " bishop", surface=SCREEN)
        board[start[5][1]][start[5][0]].putPiece(b2)

        k2 = Knight(start[6][0], start[6][1], self.team, path + "knight" + self.team + ".png",
                  pieceId=self.team + " knight", surface=SCREEN)
        board[start[6][1]][start[6][0]].putPiece(k2)

        r2 = Rook(start[7][0], start[7][1], self.team, path + "rook" + self.team + ".png",
                  pieceId=self.team + " rook", surface=SCREEN)
        board[start[7][1]][start[7][0]].putPiece(r2)

        p1 = Pawn(start[8][0], start[8][1], self.team, path + "pawn" + self.team + ".png",
                  pieceId=self.team + " pawn", surface=SCREEN)
        board[start[8][1]][start[8][0]].putPiece(p1)

        p2 = Pawn(start[9][0], start[9][1], self.team, path + "pawn" + self.team + ".png",
                  pieceId=self.team + " pawn", surface=SCREEN)
        board[start[9][1]][start[9][0]].putPiece(p2)

        p3 = Pawn(start[10][0], start[10][1], self.team, path + "pawn" + self.team + ".png",
                  pieceId=self.team + " pawn", surface=SCREEN)
        board[start[10][1]][start[10][0]].putPiece(p3)

        p4 = Pawn(start[11][0], start[11][1], self.team, path + "pawn" + self.team + ".png",
                  pieceId=self.team + " pawn", surface=SCREEN)
        board[start[11][1]][start[11][0]].putPiece(p4)

        p5 = Pawn(start[12][0], start[12][1], self.team, path + "pawn" + self.team + ".png",
                  pieceId=self.team + " pawn", surface=SCREEN)
        board[start[12][1]][start[12][0]].putPiece(p5)

        p6 = Pawn(start[13][0], start[13][1], self.team, path + "pawn" + self.team + ".png",
                  pieceId=self.team + " pawn", surface=SCREEN)
        board[start[13][1]][start[13][0]].putPiece(p6)

        p7 = Pawn(start[14][0], start[14][1], self.team, path + "pawn" + self.team + ".png",
                  pieceId=self.team + " pawn", surface=SCREEN)
        board[start[14][1]][start[14][0]].putPiece(p7)

        p8 = Pawn(start[15][0], start[15][1], self.team, path + "pawn" + self.team + ".png",
                  pieceId=self.team + " pawn", surface=SCREEN)
        board[start[15][1]][start[15][0]].putPiece(p8)


        self.pieces = [king, queen, k1, k2, b1, b2, r1, r2, p1, p2, p3, p4, p5, p6, p7, p8]
        self.king = king

    def __str__(self):
        return f"ID: {self.id} Team: {self.team}"

    def getPlayerId(self):
        return self.id

    def getPieces(self):
        return self.pieces

    def getTeam(self):
        return self.team

    # function should verify status at beginning of every turn
    def kingStatus(self):
        # if self.king.checked:
        #     self.inCheck = True
        pass

    def playerTick(self):
        pass

    def playerRender(self, screen):
        for p in self.pieces:
            p.draw()
