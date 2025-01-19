from board import Board
from os import system
from time import sleep

def main():
    input('please press enter to play') # TODO: instructions
    bd = Board()
    print(bd)

    while not game_over(bd):
        dir = input('enter your move:\n').upper()
        while not is_valid_move(bd,dir):
            dir = input('enter valid move:\n').upper() # TODO: clearer message
        clear_screen()
        bd.move(dir)
        # TODO: valid move checker, move is not valid if it doesn't more any tiles
        bd.new_tile()
        print(bd)

def instructions():
    pass

def clear_screen():
    system('clear')

def is_valid_move(bd: Board, dir: str):
    """returns where move dir is valid
        
        move is valid if it corresponds to a letter in ["W","D","S","A"] and
        if it changes the board tiles
    """

    if dir in ["W","D","S","A"]:
        old_tiles = [[tile for tile in row] for row in bd.tiles]
        bd.move(dir)
        if bd.tiles == old_tiles:
            return 0
        else:
            bd.tiles = old_tiles
            return 1
    else:
        return 0

def game_over(bd: Board):
    """returns whether board is playable or game is over

    if board is playable, returns 0 (game is not over)
    if game is over, returns 1 if board contains 2048 and 2 if there are no legal moves

    paramaters
    ----------
    bd : Board
        the current game board
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

if __name__ == "__main__":
    main()