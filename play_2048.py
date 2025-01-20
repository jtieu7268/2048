from board import Board
from os import system
from time import sleep

# TODO: documentation in board and play_2048
# TODO: testing for play_2048 functions
# TODO: continue playing after 2048
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
    while not game_over(bd):
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
            print("Here is a new board")
            continue
        clear_screen()
        score += bd.move(dir)
        bd.new_tile()     
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

def game_over(bd: Board) -> int:
    """returns whether board is playable or game is over

    if board is playable, returns 0 (game is not over)
    if game is over, returns 1 if board contains 2048 and 2 if there are no legal moves

    paramaters
    ----------
    bd : Board
        the current game board

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
                        
    if got_2048(): return 1
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