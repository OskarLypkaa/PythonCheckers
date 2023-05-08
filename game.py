from board import Checkerboard


 

check = Cheeckers(player)
comp=Computer()
check.setPieces()
check.printBoard()

while True:
    
    
    check.move()
    check.printBoard()
    comp.move()
    check.printBoard()