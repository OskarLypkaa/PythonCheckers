from board import Checkerboard
from players import HumanPlayer, ComputerPlayer
from pieces import Pieces
 
# Initialization of objects

board = Checkerboard()
piece = Pieces()

# Setting up pieces
piece.setPieces()

# Main logic of game in endless loop
while True:
    board.printBoard()
    input()

     
    #ogólnie to co teraz próbowałem zdziałać to żeby wyświetlało którową jako dużą literę i to pogrubioną
    