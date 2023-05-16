import random
import time
from board import Checkerboard


class Players(Checkerboard):

    def __init__(self, piece, queen, movePath={}, chosenPath=[]):
        self.piece = piece
        self.queen = queen
        self.movePath = movePath
        self.chosenPath = chosenPath
    def getPiece(self):
        return self.piece
    
    def getQueen(self):
        return self.queen



    def progress_bar(self, total, current, bar_length=20):
        progress = current / total
        completed_length = int(bar_length * progress)
        remaining_length = bar_length - completed_length
        completed_bar = '█' * completed_length
        remaining_bar = '-' * remaining_length
        print(f'[{completed_bar}{remaining_bar}] {progress:.1%}', end='\r', flush=True)

   

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
    def killPawn(self, move):
        if self.movePath:
            if move in self.movePath:
                for killedPawns in self.movePath[move]:
                    self.board[killedPawns] = ' '
        # Resetting values for future use
        self.movePath = {}
        self.chosenPath = []


    # Core for game movement, it contains rules of pawn movement calculated based on recuration
    def rules(self, chosenPiece, cheakBaord, deep=0):
        possibleMove=[]
        lastLoop=True

        if isinstance(self, HumanPlayer):
            if self.checkForQueen(chosenPiece):
                directions = [-7, -9, 9, 7]
                jumps = [-14, -18, 18, 14]
                limit = [7 , 15, 48, 56]
                piece = 'X'
            else:
                directions = [-7, -9]
                jumps = [-14, -18]
                limit = [7 , 15]
                piece = 'x'
        elif isinstance(self, ComputerPlayer):
            if self.checkForQueen(chosenPiece):
                directions = [ 9, 7, -7, -9]
                jumps = [18, 14, -14, -18]
                limit = [7 , 15, 48, 56]
                piece = 'X'
            else:
                directions = [9, 7]
                jumps = [18, 14]
                limit = [48 , 56]
                piece = 'o'
                    
        if deep==0 and self.movingLimit(chosenPiece, limit):
            tablelen = len(directions)//2
            for i in range(tablelen):
                if i == 1: i+=1
                if (chosenPiece + directions[i]) % 8 != 0 and cheakBaord[chosenPiece+directions[i]]==' ':
                    possibleMove.append(chosenPiece+directions[i])
                if chosenPiece % 8 != 0 and cheakBaord[chosenPiece+directions[i+1]]==' ':
                    possibleMove.append(chosenPiece+directions[i+1])

        if self.movingLimit(chosenPiece, limit, jump=True):
            tablelen = len(directions)//2
            for i in range(tablelen):
                if i == 1: i+=1
                if (chosenPiece + jumps[i]) % 8 != 0 and cheakBaord[chosenPiece+directions[i]].upper() == piece.upper() and cheakBaord[chosenPiece+jumps[i]] == ' ':               
                    self.chosenPath.append(chosenPiece+directions[i])
                    possibleMove.extend(self.rules(chosenPiece+jumps[i], cheakBaord, deep=deep+1))
                    lastLoop=False
                if chosenPiece % 8 != 0 and cheakBaord[chosenPiece+directions[i+1]].upper() == piece.upper() and cheakBaord[chosenPiece+jumps[i+1]] == ' ':
                    self.chosenPath.append(chosenPiece+directions[i+1])
                    possibleMove.extend(self.rules(chosenPiece+jumps[i+1], cheakBaord, deep=deep+1))
                    lastLoop=False


        if lastLoop and deep!=0: 
            possibleMove.append(chosenPiece)
            self.movePath[chosenPiece] = self.chosenPath[:]
            self.chosenPath.pop()
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

    # Making a queen each piece which get to the end of the border
    def makeAQueen(self, move):
        if isinstance(self, HumanPlayer) and move < 8:self.isQueen(move)
        elif isinstance(self, ComputerPlayer) and move >= 56:self.isQueen(move)
         

class HumanPlayer(Players):
    def __init__(self, piece, queen):
        super().__init__(piece, queen)

    def makeAMove(self):
        try:
            # Geting inputs of which pawn to move
            print("Choose pawn: ", end=" ")
            pawn = input()
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
            move = input()
            move = self.calculatePosition(move)
            self.checkIfMoveIsLegal(move, highlighted)
            
            # Finally moving a piece and checking if it's a queen or not
            if self.board[pawn].isupper():self.move(move, pawn, True)
            else: self.move(move, pawn)
        except:
            print("Incorrect input!")          
            time.sleep(1)
            # Resetting values for future use
            self.movePath = {}
            self.chosenPath = []
            self.printBoard() 
            self.makeAMove()

    # Deleting old position of piece and placing it in a new, chosen one
    def move(self, move, pawn, isaQueen=None):
        self.board[pawn]=' '
        if isaQueen:self.board[move]=self.queen
        else: self.board[move]=self.piece
        self.killPawn(move)
        self.makeAQueen(move)

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

        print("Computer is thinking")
        total_items = 100
        for i in range(total_items + 1):
            self.progress_bar(float(total_items), float(i))
            time.sleep(0.02)

    # Deleting old position of piece and placing it in a new, chosen one
    def move(self, move, pawn, isaQueen=None):
        self.board[pawn]=' '
        if isaQueen:self.board[move]=self.queen
        else: self.board[move]=self.piece
        self.killPawn(move)
        self.makeAQueen(move)

    def minimax(self, board, depth, is_maximizing_player):
        pass