from board import Checkerboard
from pieces import Pieces
from players import HumanPlayer, ComputerPlayer



def main():
    # Initialization of objects
    board = Checkerboard()
    piece = Pieces()
    player = HumanPlayer('o','O')
    computer = ComputerPlayer('x','X')
    # Setting up pieces
    piece.setPieces()

    # Main logic of game in endless loop
    while True:
        board.printBoard()
        player.makeAMove()
        board.printBoard()
        computer.makeAMove()

if __name__ == "__main__":
    main()