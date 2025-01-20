from board import Board
from os import system
from time import sleep

# TODO: optimizations: is_valid_move
# TODO: board as row and col of linked lists

def main():
    bd = Board()
    game_start(bd)
    score = game_loop(bd)
    game_end(score)

def clear_screen():
    system('clear')

def game_start(bd: Board):
    """introduces game through print statements

    welcomes player into game
    prompts player to acknowlege by pressing any key
    clears terminal screen
    """

    print("Welcome to 2048!")
    input("To start, press any key\n")
    clear_screen()

def game_loop(bd: Board) -> int:
    """main game loop which iteratively requests command or move direction from player, moves tiles, and tracks score

    parameters
    ----------
    bd : Board
        the game board

    returns
    -------
    int
        represents the score of the game i.e. the sum of all merged tiles during the game
    """

    score = 0
    status = game_over_status(bd)
    won = False
    while status != 2:
        if status == 1:
            won = True
            print("Congratulations, you got 2048!")
            input("Press any key to continue\n")
        print(f"SCORE: {score}")
        print(bd)
        print("OPTIONS")
        print("(W) UP\n(D) RIGHT\n(S) DOWN\n(A) LEFT\n(Q) QUIT\n(R) RESTART")
        dir = input('Enter your move:\n').upper()
        while dir != "Q" and dir != "R" and not is_valid_move(bd,dir):
            dir = input('Enter a valid move:\n').upper()
        if dir == "Q":
            break
        if dir == "R":
            clear_screen()
            bd = Board()
            score = 0
            print("Here is a new board")
            continue
        clear_screen()
        score += bd.move(dir)
        bd.new_tile()
        status = game_over_status(bd,won)
    return score   

def is_valid_move(bd: Board, dir: str) -> bool:
    """returns whether move dir is valid
        
    move is valid if it corresponds to a letter in ["W","D","S","A"] and if it changes the board tiles

    prints a message to clarify how to make move valid
    
    parameters
    ----------
    bd : Board
        the game board
    dir : str
        the input from player

    returns
    -------
    bool
        True if dir is a valid move, else False

    """

    if dir in ["W","D","S","A"]:
        old_tiles = [[tile for tile in row] for row in bd.tiles]
        bd.move(dir)
        if bd.tiles == old_tiles:
            print("Your move did not move any tiles. Please select another direction.")
            return False
        else:
            bd.tiles = old_tiles
            return True
    else:
        print("That is not a valid option. Please refer to the options above.")
        return False

def game_over_status(bd: Board, won: bool=False) -> int:
    """returns status of the game board

    if board is playable, returns 0 (game is not over) or returns 1 if board contains 2048
    if game is over, returns 2 (there are no legal moves)

    paramaters
    ----------
    bd : Board
        the current game board
    won : bool
        boolean indicating whether game has been won i.e. if 2048 tile has been created

    returns
    -------
    int
        the status of the game, 0 if game is not over, 1 if board contains 2048, 2 if there are no legal moves
    """

    def is_in_board(val: int):
        return any(val in row for row in bd.tiles)
    
    def got_2048():
        return is_in_board(2048)
        
    def no_legal_moves():
        # checks if board is filled
        if is_in_board(0): 
            return 0
        # board is filled, checks if there are possible merges
        else:
            for orientation in [bd.tiles,zip(*bd.tiles)]:
                for vector in orientation:
                    prev_val_pos = -1
                    for i,tile in enumerate(vector):
                        if prev_val_pos != -1 and tile == vector[prev_val_pos]:
                            return 0
                        prev_val_pos = i
            return 1
                        
    if not won and got_2048(): return 1
    if no_legal_moves(): return 2
    return 0

def game_end(score: int):
    """displays score of the game and bids adieu to player through print statements

    """

    clear_screen()
    print(f'Your score was {score}')
    print("Thanks for playing!")

if __name__ == "__main__":
    main()