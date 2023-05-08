from board import Checkerboard


 
# Initialization of object
board = Checkerboard()


# Main logic of game in endless loop
while True:
    board.move(player)
    board.printBoard()
    board.move(computer)
    board.printBoard()