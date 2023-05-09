import time
from board import Checkerboard


class Players(Checkerboard):

    def __init__(self, piece, queen):
        self.piece = piece
        self.queen = queen

    def getPiece(self):
        return self.piece
    
    def getQueen(self):
        return self.queen

    def move(self):
        try:
            # Geting inputs of which pawn to move and which square to go
            print("Choose pawn: ", end=" ")
            pawn=input()
            pawn = self.calculatePosition(pawn)
            self.checkIfPawnIsLegal(pawn)

            print("Choose move: ", end=" ")
            move=input()
            move = self.calculatePosition(move)
            self.checkIfMoveIsLegal(move)

        except:
            print("Incorrect move!")          
            time.sleep(2) 

    # Calculating position of choosen square. Changing e.g. c2 to 57 which is id of a board
    def calculatePosition(self, pawn):
        col = ord(pawn[:1])-96
        row = abs(int(pawn[-1:])-9)
        chosenSquare = 8*(row-1)+col-1
        return chosenSquare

    def checkIfPawnIsLegal(self, pawn):
        if self.board[pawn]=='O' or self.board[pawn]=='o':
            return True 
        else: raise ValueError

    def checkIfMoveIsLegal(self, move, pawn):
        possibleMoves=self.rules(pawn, self.board)
        if move in possibleMoves:
            return True
        else: raise ValueError

    def rules(self, chosenPiece, cheakBaord, comp='X',deep=0):
        possibleMove=[]
        if comp == 'X':
            directions = [-7, -9]
            jumps = [-14, -18]
            limit = [7 , 15]
        else:
            directions = [7, 9]
            jumps = [14, 18]
            limit = [7 , 15]

                
        if deep==0 and chosenPiece > limit[0]:
            if chosenPiece + directions[0] % 8 != 0 and cheakBaord[chosenPiece+directions[0]]==' ':
                possibleMove.append(chosenPiece+directions[0])
            if chosenPiece % 8 != 0 and cheakBaord[chosenPiece+directions[1]]==' ':
                possibleMove.append(chosenPiece+directions[1])
        if chosenPiece > limit[1]:
            if chosenPiece + jumps[0] % 8 != 0 and cheakBaord[chosenPiece+directions[0]].upper() == comp and cheakBaord[chosenPiece+jumps[0]] == ' ':               
                possibleMove.append(chosenPiece+jumps[0])
                possibleMove.extend(self.rules(chosenPiece+jumps[0], cheakBaord, deep=deep+1))
            if chosenPiece % 8 != 0 and cheakBaord[chosenPiece+directions[1]].upper() == comp and cheakBaord[chosenPiece+jumps[1]] == ' ':
                possibleMove.append(chosenPiece+jumps[1])
                possibleMove.extend(self.rules(chosenPiece+jumps[1], cheakBaord, deep=deep+1))
        return possibleMove


class HumanPlayer(Players):
    def __init__(self, piece, queen):
        super().__init__(piece, queen)

class ComputerPlayer(Players):
    def __init__(self, piece, queen):
        super().__init__(piece, queen)