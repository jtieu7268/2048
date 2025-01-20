from board import Board
from os import system
from time import sleep

# TODO: game instructions
# TODO: score
# TODO: continue playing after 2048
# TODO: polish main method
# TODO: polishing look
# TODO: end game screen
# TODO: optimizations: is_valid_move
# TODO: board as row and col of linked lists

def main():
    bd = Board()
    game_start(bd)
    game_loop(bd)
    game_end()

def clear_screen():
    system('clear')

def game_start(bd: Board):
    print("Welcome to 2048!")
    input("To start, press any key\n")
    clear_screen()

def game_loop(bd: Board):
    while not game_over(bd):
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
        bd.move(dir)
        bd.new_tile()        

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

def game_end():
    clear_screen()
    print("Thanks for playing!")

if __name__ == "__main__":
    main()