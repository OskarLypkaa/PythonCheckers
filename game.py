from board import Checkerboard
from pieces import Pieces
from players import HumanPlayer
# Initialization of objects

board = Checkerboard()
piece = Pieces()
player = HumanPlayer('o','O')
# Setting up pieces
piece.setPieces()

# Main logic of game in endless loop
while True:
    board.printBoard()
    player.move()

