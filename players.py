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
                piece = 'O'
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

    def makeAMove(self):
        best_move = self.minimax(self.board, 4, True)[1]  # Wywołanie algorytmu Minimax z maksymalną głębokością 4
        self.move(best_move[1], best_move[0])

    def minimax(self, board, depth, is_maximizing_player):
        if depth == 0 or self.isGameOver(board):
            return self.evaluate(board), None

        if is_maximizing_player:
            max_eval = float('-inf')
            best_move = None
            possible_moves = self.getAllPossibleMoves(board, self.piece)
            for move in possible_moves:
                new_board = self.getNewBoardAfterMove(board, move[0], move[1])
                evaluation = self.minimax(new_board, depth - 1, False)[0]
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            possible_moves = self.getAllPossibleMoves(board, self.computer)
            for move in possible_moves:
                new_board = self.getNewBoardAfterMove(board, move[0], move[1])
                evaluation = self.minimax(new_board, depth - 1, True)[0]
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move
            return min_eval, best_move

    def evaluate(self, board):
        player_score = 0
        computer_score = 0

        for i in range(len(board)):
            if board[i] == self.piece or board[i] == self.queen:
                player_score += 1
            elif board[i] == self.computer or board[i] == self.computer.upper():
                computer_score += 1

        return player_score - computer_score

    def getAllPossibleMoves(self, board, player):
        possible_moves = []
        for i in range(len(board)):
            if board[i] == player:
                moves = self.rules(i, board)
                for move in moves:
                    possible_moves.append((i, move))
        return possible_moves

    def getNewBoardAfterMove(self, board, start, end):
        new_board = board[:]
        new_board[start] = ' '
        new_board[end] = self.piece if self.piece.isupper() else self.queen
        self.killPawn(end)
        self.makeAQueen(end)
        return new_board

    def isGameOver(self, board):
        player_moves = self.getAllPossibleMoves(board, self.piece)
        computer_moves = self.getAllPossibleMoves(board, self.piece.upper())

        return len(player_moves) == 0 or len(computer_moves) == 0