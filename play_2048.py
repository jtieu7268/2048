from board import Board
from os import system

def clear_screen():
    system('clear')

class Game:

    MOVE_KEY = {"W":"U",
                "D":"R",
                "S":"D",
                "A":"L"}
    GAME_KEY = ["W","D","S","A","R","Q"]
    WIN_VAL_OPTIONS = ["2048", "1024", "512", "256", "128"]
    BOARD_STATE_KEY = {0: "PLAY",
                       1: "WIN",
                       2: "END",
                       3: "QUIT"}

    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.won = False
        self.start()
        self.reset()
        self.loop()

    def start(self):
        """introduces game through print statements and sets up game

            welcomes player into game
            prompts player to acknowlege by pressing any key
            clears terminal screen
        """

        print("Welcome to 2048!")
        input("To start, press any key\n")
        clear_screen()

    def reset(self):
        """prompts player to enter win value and initializes board accordingly

        """
        
        if self.score > self.high_score:
            self.high_score = self.score
        self.score = 0
       
        print("What do you want to be the win value?")
        win_val = input(f"Please enter one of the following or press enter to use default (2048): {self.WIN_VAL_OPTIONS}\n")
        while win_val != "" and win_val not in self.WIN_VAL_OPTIONS:
            win_val = input(f"Please enter a valid option or press enter to use default (2048): {self.WIN_VAL_OPTIONS}\n")
        if win_val == "": 
            self.board = Board()
            self.WIN_VAL = 2048
        else: 
            self.WIN_VAL = int(win_val)
            self.board = Board(win_val=self.WIN_VAL)
        self.won = False

        clear_screen()

    def loop(self):
        status = self.board.is_end()
        while self.BOARD_STATE_KEY[status] != "END":
            if self.BOARD_STATE_KEY[status] == "WIN":
                self.won = True
                print(f"Congratulations, you got {self.WIN_VAL}!")
                input("Press any key to continue playing\n")
                clear_screen()

            print(f"SCORE: {self.score}\tHIGH SCORE: {self.high_score}")
            print(self.board)
            print("OPTIONS")
            print("(W) UP\n(D) RIGHT\n(S) DOWN\n(A) LEFT\n(Q) QUIT\n(R) RESTART\n")
            
            dir = input('Enter your move:\n').upper()
            while dir not in self.GAME_KEY or (dir in self.MOVE_KEY and not self.board.is_valid_move(self.MOVE_KEY[dir])):
                if dir not in self.GAME_KEY:
                    print("That is not a valid option. Please refer to the options above.")
                else:
                    print("Your move did not move any tiles. Please select another direction.")
                dir = input('Enter a valid move:\n').upper()
            if dir == "Q":
                status = 3
                break
            if dir == "R":
                clear_screen()
                self.reset()
                status = self.board.is_end()
                print("Here is a new board")
                continue
            
            clear_screen()
            self.score += self.board.move(self.MOVE_KEY[dir])
            self.board.new_tile()
            status = self.board.is_end(self.won)
            if self.score > self.high_score: self.high_score = self.score
        
        if self.BOARD_STATE_KEY[status] == "QUIT":
            self.end(manual_quit=True)
        else:
            self.end()

    def end(self,manual_quit: bool=False):
        """displays score of the game and asks if player wants to play again, restarts game or bids adieu to player through print statements

        """

        clear_screen()
        if not manual_quit: print('GAME OVER')
        print(f'Your high score was {self.high_score}')
        print("Thanks for playing! ")
        if not manual_quit:
            ans = input("Would you like to play again? y or n\n").upper()
            while ans != "Y" and ans != "N":
                ans = input("Please try again. Would you like to play again? y or n\n").upper()
            if ans == "Y": 
                self.reset()
                self.loop()
            else:
                clear_screen()
                print("Thanks for playing!")

if __name__ == "__main__":
    game = Game()