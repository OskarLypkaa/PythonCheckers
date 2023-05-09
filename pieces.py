from colorama import init, Fore, Back, Style
from board import Checkerboard
from players import HumanPlayer, ComputerPlayer

class Pieces(Checkerboard):
    player = HumanPlayer('o','O')
    computer = ComputerPlayer('x','X')

    # Initialization of colorama packet
    init()

    def setPieces(self):
        for i in range(16):
            if i // 8 % 2 == 0:
                if i%2==0: self.board[i]=self.computer.getPiece()
            elif i // 8 % 2 == 1:
                if i%2==1: self.board[i]=self.computer.getPiece()

        for i in range(48, 64):
            if i // 8 % 2 == 0:
                if i%2==0: self.board[i]=self.player.getPiece()
            elif i // 8 % 2 == 1:
                if i%2==1: self.board[i]=self.player.getPiece()

    