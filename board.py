import os
import math
from colorama import init, Fore, Back, Style

class Checkerboard():


    # Initialization of colorama packet
    init()

    # Initializaton of board list 
    board = [
        ' ',' ',' ',' ',' ',' ',' ',' ',
        ' ',' ',' ',' ',' ',' ',' ',' ',
        ' ',' ',' ',' ',' ',' ',' ',' ',
        ' ',' ',' ',' ',' ',' ',' ',' ',
        ' ',' ',' ',' ',' ',' ',' ',' ',
        ' ',' ',' ',' ',' ',' ',' ',' ',
        ' ',' ',' ',' ',' ',' ',' ',' ',
        ' ',' ',' ',' ',' ',' ',' ',' '
        ]
        
    # Basic methode for printing board
    def printBoard(self, highlited=['']):
        # Clearing the screen
        os.system('cls')
        print('Checkers Game!\n'+Style.BRIGHT)
        
        # Printing borders surrounding board
        self.printBorder()

        # Listing true each element of board element in order to display it properly 
        for i in range(64):
            # If statment responsible for printing border in sides of board
            if (i + 1) % 8 == 1: print(Back.MAGENTA +  str(abs(math.floor((i+1)/8)-8)), end=" " + Fore.RESET)

            # Logic responsible for displaying the board in correct pattern
            if not i in highlited:
                # checking for upper and lover case chars in order to display bolder char (as queen)
                if self.board[i]==' ':                   
                    if i // 8 % 2 == 0:
                        if i % 2 == 0:print(Back.WHITE + self.board[i], end=" " + Fore.RESET)
                        else:print(Back.CYAN + self.board[i], end=" " + Fore.RESET)
                    elif i // 8 % 2 == 1:
                        if i % 2 == 0:print(Back.CYAN + self.board[i], end=" " + Fore.RESET)
                        else:print(Back.WHITE + self.board[i], end=" " + Fore.RESET)
                # Printing queen as an uppercase and bold
                elif self.board[i].isupper:print(Back.WHITE + Style.BRIGHT + self.board[i], end=" " + Fore.RESET)                        
            else: 
                if highlited[0]==i :print(Back.RED + self.board[i], end=" " + Fore.RESET)
                else: print(Back.GREEN + self.board[i], end=" " + Fore.RESET)

            # If statment responsible for printing border in sides of board
            if (i + 1) % 8 == 0 and not i == 0:print(Back.MAGENTA + str(abs(math.floor((i+1)/8)-9))+' ' + Fore.RESET)

        # Printing borders surrounding board
        self.printBorder()
        # Resetting terminal color back to black
        print(Back.BLACK + Fore.RESET)

    def isQueen(self, number):
        self.board[number] = self.board[number].upper()

    def printBorder(self):
        print(Back.MAGENTA + ' ', end=" " + Fore.RESET)
        # Printing letters form asci code 
        for i in range(97,105):     
            print(Back.MAGENTA + chr(i), end=" " + Fore.RESET)
        print(Back.MAGENTA + '  ' + Fore.RESET)