from pieceSub import *

class Player():

    def __init__(self, playerId, team, start, SCREEN):
        print("In init")
        self.id = playerId
        self.team = team # team needs to be capitalized for graphic path

        # if checked, valid moves are restricted to unchecking
        self.inCheck = False

        path = "./graphics/pieces/" + team.lower() + "/"

        r1 = Rook(start[0][0], start[0][1], self.team, path + "rook" + self.team + ".png",
                  self.team + " rook", SCREEN)

        k1 = Knight(start[1][0], start[1][1], self.team, path + "knight" + self.team + ".png",
                  self.team + " knight", SCREEN)

        b1 = Bishop(start[2][0], start[2][1], self.team, path + "bishop" + self.team + ".png",
                  self.team + " bishop", SCREEN)

        queen = Queen(start[3][0], start[3][1], self.team, path + "queen" + self.team + ".png",
                  self.team + " queen", SCREEN)

        king = King(start[4][0], start[4][1], self.team, path + "king" + self.team + ".png",
                  self.team + " king", SCREEN)

        b2 = Bishop(start[5][0], start[5][1], self.team, path + "bishop" + self.team + ".png",
                  self.team + " bishop", SCREEN)

        k2 = Knight(start[6][0], start[6][1], self.team, path + "knight" + self.team + ".png",
                  self.team + " knight", SCREEN)

        r2 = Rook(start[7][0], start[7][1], self.team, path + "rook" + self.team + ".png",
                  self.team + " rook", SCREEN)

        p1 = Pawn(start[8][0], start[8][1], self.team, path + "pawn" + self.team + ".png",
                  self.team + " pawn", SCREEN)

        p2 = Pawn(start[9][0], start[9][1], self.team, path + "pawn" + self.team + ".png",
                  self.team + " pawn", SCREEN)

        p3 = Pawn(start[10][0], start[10][1], self.team, path + "pawn" + self.team + ".png",
                  self.team + " pawn", SCREEN)

        p4 = Pawn(start[11][0], start[11][1], self.team, path + "pawn" + self.team + ".png",
                  self.team + " pawn", SCREEN)

        p5 = Pawn(start[12][0], start[12][1], self.team, path + "pawn" + self.team + ".png",
                  self.team + " pawn", SCREEN)

        p6 = Pawn(start[13][0], start[13][1], self.team, path + "pawn" + self.team + ".png",
                  self.team + " pawn", SCREEN)

        p7 = Pawn(start[14][0], start[14][1], self.team, path + "pawn" + self.team + ".png",
                  self.team + " pawn", SCREEN)

        p8 = Pawn(start[15][0], start[15][1], self.team, path + "pawn" + self.team + ".png",
                  self.team + " pawn", SCREEN)


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
