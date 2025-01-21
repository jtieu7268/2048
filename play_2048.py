from board import Board
from os import system
from time import sleep

move_key = {"W":"U",
            "D":"R",
            "S":"D",
            "A":"L"}
game_key = ["W","D","S","A","R","Q"]
win_val_options = ["2048", "1024", "512", "256", "128"]

def main():
    game_start()
    score = game_loop()
    game_end(score)

def clear_screen():
    system('clear')

def game_start():
    """introduces game through print statements

    welcomes player into game
    prompts player to acknowlege by pressing any key
    clears terminal screen
    """

    print("Welcome to 2048!")
    input("To start, press any key\n")
    clear_screen()

def game_loop() -> int:
    """main game loop which iteratively requests command or move direction from player, moves tiles, and tracks score

    returns
    -------
    int
        represents the score of the game i.e. the sum of all merged tiles during the game
    """

    print("What do you want to be the win value?")
    win_val = input("Please enter one of the following or press enter to use default (2048): [2048, 1024, 512, 256, 128]\n")
    while win_val != "" and win_val not in win_val_options:
        win_val = input("Please enter a valid option or press enter to use default (2048): [2048, 1024, 512, 256, 128]\n")
    if win_val == "": 
        bd = Board()
        win_val = 2048
    else: 
        win_val = int(win_val)
        bd = Board(win_val=win_val)
    high_score = score = 0
    status = bd.is_end()
    won = False
    while status != 2:
        if status == 1:
            won = True
            print(f"Congratulations, you got {win_val}!")
            input("Press any key to continue\n")
            clear_screen()
        print(f"SCORE: {score}")
        print(bd)
        print("OPTIONS")
        print("(W) UP\n(D) RIGHT\n(S) DOWN\n(A) LEFT\n(Q) QUIT\n(R) RESTART")
        dir = input('Enter your move:\n').upper()
        while dir not in game_key or (dir in move_key and not bd.is_valid_move(move_key[dir])):
            if dir not in game_key:
                print("That is not a valid option. Please refer to the options above.")
            else:
                print("Your move did not move any tiles. Please select another direction.")
            dir = input('Enter a valid move:\n').upper()
        if dir == "Q":
            break
        if dir == "R":
            clear_screen()
            bd = Board()
            if score > high_score: high_score = score
            score = 0
            print("Here is a new board")
            continue
        clear_screen()
        score += bd.move(move_key[dir])
        bd.new_tile()
        status = bd.is_end(won)
    if score > high_score: high_score = score
    return high_score

def game_end(score: int):
    """displays score of the game and bids adieu to player through print statements

    """

    clear_screen()
    print(f'Your high score was {score}')
    print("Thanks for playing!")

if __name__ == "__main__":
    main()