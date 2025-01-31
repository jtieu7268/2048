"""2048 game with text-based interface through terminal."""

from board import Board, BoardStatus, Move
from os import system
from enum import Enum

def clear_screen():
    system('clear')

class GameStatus(Enum):
    PLAY = 0
    QUIT = 3

class Game:
    """game manager for playing 2048.

    Attributes
    ----------
    MOVE_KEY : dict[str, Move]
        keys for game associated with their direction
    
    GAME_KEY : list[str]
        valid keys for playing game
    
    WIN_VAL_OPTIONS : list[str]
        options for game win values
    
    score : int
        current game score
    
    high_score : int
        high score from all games played during session
    
    won : bool
        whether the game is won
    
    board : Board
        the board associated with the game
    
    WIN_VAL : int
        the win value of the current session
    
    Methods
    -------
    start()
        introduces the game through print statements and sets up the game
    
    reset()
        starts a new game, asks player for new win value and initializes board accordingly
    
    loop()
        the game loop for each new game
    
    end()
        displays score of the game and asks if player wants to play again, restarts game or bids adieu to player through print statements

    """

    MOVE_KEY = {"W":Move.UP,
                "D":Move.RIGHT,
                "S":Move.DOWN,
                "A":Move.LEFT}
    GAME_KEY = ("W","D","S","A","R","Q")
    WIN_VAL_OPTIONS = ("2048", "1024", "512", "256", "128", "64", "32", "16")

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
        """prompts player to enter win value and initializes board accordingly."""
        
        if self.score > self.high_score:
            self.high_score = self.score
        self.score = 0
       
        print("What do you want to be the win value?")
        print("Please enter one of the following or press enter to use default (2048):")
        for i, win_val in enumerate(self.WIN_VAL_OPTIONS):
            print(f"[{i+1}] {int(win_val)}")
        win_val = input()
        
        while win_val != "" and not ((win_val in self.WIN_VAL_OPTIONS) or (win_val in [f"{x}" for x in range(1,len(self.WIN_VAL_OPTIONS)+1)])):
            print("Please enter a valid option or press enter to use default (2048):")
            for i, win_val in enumerate(self.WIN_VAL_OPTIONS):
                print(f"[{i+1}] {int(win_val)}")
            win_val = input()
        
        if win_val == "": 
            # default win value
            self.WIN_VAL = 2048
        elif win_val in self.WIN_VAL_OPTIONS: 
            # literal win value was entered
            self.WIN_VAL = int(win_val)
        else:
            # numbered option for win value was entered
            self.WIN_VAL = int(self.WIN_VAL_OPTIONS[int(win_val)-1])
        
        self.board = Board(win_val=self.WIN_VAL)
        self.won = False

        clear_screen()

    def loop(self):
        """the game loop."""

        status = self.board.is_end()
        while status != BoardStatus.GAMEOVER:
            if status == BoardStatus.WIN:
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
                status = GameStatus.QUIT
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
        
        if status == GameStatus.QUIT:
            self.end(manual_quit=True)
        else:
            self.end()

    def end(self,manual_quit: bool=False):
        """displays score of the game and asks if player wants to play again, restarts game or bids adieu to player through print statements."""

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