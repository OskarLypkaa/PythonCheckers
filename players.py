import random
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

    def checkIfMoveIsLegal(self, move, moves):
        if move in moves:
            return True
        else: raise ValueError

    # This methode wont work, it has to be corrected
    def killPawn(self, pawn):
        self.board[pawn] = ' '

    # Core for game movement, it contains rules of pawn movement calculated based on recuration
    def rules(self, chosenPiece, cheakBaord, deep=0):
        possibleMove=[]
        if isinstance(self, HumanPlayer):
            directions = [-7, -9]
            jumps = [-14, -18]
            limit = [7 , 15]
            piece = 'x'
        elif isinstance(self, ComputerPlayer):
            directions = [9, 7]
            jumps = [18, 14]
            limit = [48 , 56]
            piece = 'o'
                
        if deep==0 and self.movingLimit(chosenPiece, limit):
            if chosenPiece + directions[0] % 8 != 0 and cheakBaord[chosenPiece+directions[0]]==' ':
                possibleMove.append(chosenPiece+directions[0])
            if chosenPiece % 8 != 0 and cheakBaord[chosenPiece+directions[1]]==' ':
                possibleMove.append(chosenPiece+directions[1])
        if self.movingLimit(chosenPiece, limit, jump=True):
            if chosenPiece + jumps[0] % 8 != 0 and cheakBaord[chosenPiece+directions[0]].upper() == piece.upper() and cheakBaord[chosenPiece+jumps[0]] == ' ':               
                possibleMove.append(chosenPiece+jumps[0])
                self.killPawn(chosenPiece+directions[0])
                possibleMove.extend(self.rules(chosenPiece+jumps[0], cheakBaord, deep=deep+1))
            if chosenPiece % 8 != 0 and cheakBaord[chosenPiece+directions[1]].upper() == piece.upper() and cheakBaord[chosenPiece+jumps[1]] == ' ':
                possibleMove.append(chosenPiece+jumps[1])
                self.killPawn(chosenPiece+directions[0])
                possibleMove.extend(self.rules(chosenPiece+jumps[1], cheakBaord, deep=deep+1))
        return possibleMove

    # Checking if pawn is close to the end of a board in order to prevent errors
    def movingLimit(self, piece, limit, jump=False):
        if isinstance(self, HumanPlayer):
            if not jump:
                if piece > limit[0]: return True
            else:
                if piece > limit[1]: return True
            return False
        elif isinstance(self, ComputerPlayer):
            if not jump:
                if piece < limit[0]: return True
            else:
                if piece < limit[1]: return True
            return False

class HumanPlayer(Players):
    def __init__(self, piece, queen):
        super().__init__(piece, queen)

    def makeAMove(self):
        try:
            # Geting inputs of which pawn to move
            print("Choose pawn: ", end=" ")
            pawn=input()
            pawn = self.calculatePosition(pawn)
            self.checkIfPawnIsLegal(pawn)

            # Highlighting possible moves
            highlighted = []
            highlighted.append(pawn)
            highlighted.extend(self.rules(pawn, self.board))
            # Printing board again but with highlighted moves
            self.printBoard(highlighted)

            # Geting inputs of which square to go
            print("Choose move: ", end=" ")
            move=input()
            move = self.calculatePosition(move)
            self.checkIfMoveIsLegal(move, highlighted)
            
            # Finally moving a piece
            self.move(move, pawn)
        except:
            print("Incorrect move!")          
            time.sleep(2) 

    # Deleting old position of piece and placing it in a new, chosen one
    def move(self, move, pawn, isaQueen=None):
        self.board[pawn]=' '
        if isaQueen:self.board[move]=self.queen
        else: self.board[move]=self.piece
        
class ComputerPlayer(Players):
    def __init__(self, piece, queen):
        super().__init__(piece, queen)

    # Begining of an AI, now computer is listing all of the possible moves and chosing it randomly
    def makeAMove(self):
        while True:
            random_pawn = random.randint(0, 63)
            if self.board[random_pawn] == self.piece or self.board[random_pawn] == self.queen:
                possible_moves = self.rules(random_pawn, self.board)
                if possible_moves: break
        new_pos = random.choice(possible_moves)
        self.move(new_pos, random_pawn)

    # Deleting old position of piece and placing it in a new, chosen one
    def move(self, move, pawn, isaQueen=None):
        self.board[pawn]=' '
        if isaQueen:self.board[move]=self.queen
        else: self.board[move]=self.piece