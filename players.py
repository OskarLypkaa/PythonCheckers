from colorama import init, Fore, Back, Style

class Players():
    # Initialization of colorama packet
    init()

    def __init__(self, piece, queen):
        self.piece = piece
        self.queen = queen

    def getPiece(self):
        return self.piece
    
    def getQueen(self):
        return self.queen
    # Pamiętać, że to nie do końca działa
    def printPawn(self, boardNumber):
        print(Back.WHITE + Style.BRIGHT +self.board[boardNumber], end=" " + Fore.RESET)
    
    def printQueen(self, boardNumber):
        print(Back.WHITE + Style.BRIGHT + self.board[boardNumber], end=" " + Fore.RESET)

class HumanPlayer(Players):
    def __init__(self, piece, queen):
        super().__init__(piece, queen)

class ComputerPlayer(Players):
    def __init__(self, piece, queen):
        super().__init__(piece, queen)