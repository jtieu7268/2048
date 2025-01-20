from random import choice
from collections import deque
import math

class Board:
    """a class representing board for playing 2048

    attributes
    ----------
    tiles : list
        the tiles of the board represented as a 2d array
    DIM : int
        the dimension of each side of the board
    START_VALS : list
        a list of possible values for new tiles on the board
    WIN_VAL : int
        the value of the tile to form to win
    MOVES : str
        valid moves: U: UP, R: RIGHT, D: DOWN, L: LEFT
    
    methods
    -------
    transpose(tiles: list) -> list
        returns a copy of tiles transposed
    reverse(tiles: list) -> list
        returns a copy of tiles reversed left to right
    process_tiles(dir: str) -> list
        processes board tiles based on direction dir so move related methods can be applied generally independent of direction
    unprocess_tiles(tiles: list, dir: str) -> tiles
        unprocesses tiles based on direction dir to restore tiles into original board tiles orientation
    is_valid_move(dir: str) -> bool
        returns whether moving tiles in direction dir results in a change in the board tiles    
    new_tile()
        generates a new tile with a start value at an open location on the board
    move(dir: str) -> int
        modifies board tiles according to direction dir, generates new tile if possible, returns score from move
    is_end()
        # TODO: implement and decide if want to separate
    """

    DIM = 4
    START_VALS = [2] * 9 + [4] # 90% prob of 2, 10% prob of 1
    MOVES = ["U","R","D","L"]

    def __init__(self, win_val: int = 2048):
        
        self.tiles = [[0] * self.DIM for _ in range(self.DIM)]
        self.WIN_VAL = win_val
        
        # generate first two tiles
        self.new_tile()
        self.new_tile()
    
    def transpose(tiles: list) -> list:
        """returns a copy of tiles transposed

        parameters
        ----------
        tiles : list
            2d array

        returns
        -------
        list
            tiles transposed
        """

        return list(map(list,zip(*tiles)))
        
    def reverse(tiles: list) -> list:
        """returns a copy of tiles reversed left to right

        parameters
        ----------
        tiles : list
            2d array
        
        returns
        -------
        list
            tiles reversed left to right

        """

        return [vector[::-1] for vector in tiles]

    def process_tiles(self, dir: str) -> list:
        """processes board tiles based on direction dir so move-related methods can be applied generally independent of direction

        parameters
        ----------
        dir : str
            represents direction of move, is one of MOVES

        returns
        -------
        list
            a copy of board tiles transposed and/or reversed based on dir
        """

        tiles = self.tiles
        if dir == "U" or dir == "D":
            tiles = Board.transpose(tiles)
        if dir == "R" or dir == "D":
            tiles = Board.reverse(tiles)
        return tiles

    def unprocess_tiles(self, tiles: list, dir: str) -> list:
        """unprocesses tiles based on direction dir to restore tiles into original board tiles orientation

        parameters
        ----------
        tiles : list
            the previously processed board tiles
        dir : str
            the direction of the move upon which the previous processing was based, is one of MOVES

        returns
        -------
        list
            a copy of tiles transposed and/or reversed to undo previous processing based on dir
        """

        if dir == "R" or dir == "D":
            tiles = Board.reverse(tiles)
        if dir == "U" or dir == "D":
            tiles = Board.transpose(tiles)
        return tiles

    def is_valid_move(self, dir: str) -> bool:
        """checks that move is valid, i.e., moving tiles yields a change to board tiles

        parameters
        ----------
        dir : str
            direction of the move to be applied to board tiles, is one of MOVES

        returns
        bool
            whether a move in direction dir applied to board tiles results in a change in the board tiles
        """

        tiles = self.process_tiles(dir)
        for i, vector in enumerate(tiles):
            for j, tile in enumerate(vector[:-1]):
                # tile would be moved
                if tile == 0 and vector[j+1] != 0:
                    return True
                # tile would be merged
                if tile != 0 and vector[j+1] == tile:
                    return True
        return False

    def new_tile(self):
        """generates a new tile with a start value at an open location on the board

        directly modifies board tiles
        """
        
        # generate random position from open positions on the board
        r,c = choice([(i,j) for i in range(self.DIM) for j in range(self.DIM) if self.tiles[i][j] == 0])

        # generate random value from start values
        self.tiles[r][c] = choice(self.START_VALS)

    def move(self,dir: str) -> int:
        """modifies board tiles according to direction dir, generates new tile if possible

        tiles slide in chosen direction based on the following:
	        1. tiles slide until stopped by edge of board
	        2. if two tiles of the same number collide, they merge to form a tile with the value of their sum
	        3. if three tiles with the same value collide, only the two farthest into the chosen direction merge
	        4. if four tiles with the same value collide, the first two and the last two merge

        parameters
        ----------
        dir : str
            the direction to move tiles, dir is in MOVES
            "U": UP
            "R": RIGHT
            "D": DOWN
            "L": LEFT

        returns
        -------
        int
            the sum of all the merged tiles resulting from moving tiles in direction dir
        """

        tiles = self.process_tiles(dir)
        score = 0
    
        for i, vector in enumerate(tiles):
            empty_queue = deque()
            prev_tile_pos = -1
            for j, tile in enumerate(vector):
                # empty tile
                if not tile:
                    empty_queue.append(j)
                # tile exists
                else:
                    # merge
                    if prev_tile_pos != -1 and tiles[i][prev_tile_pos] == tile:
                        tiles[i][prev_tile_pos] *= 2
                        score += tiles[i][prev_tile_pos]
                        tiles[i][j] = 0
                        empty_queue.append(j)
                        prev_tile_pos = -1
                    # move tile to furthest empty space to the left
                    else:
                        if empty_queue:
                            new_j = empty_queue.popleft()
                            tiles[i][new_j] = tile
                            tiles[i][j] = 0
                            empty_queue.append(j)
                            prev_tile_pos = new_j
                        else:
                            prev_tile_pos = j
        
        self.tiles = self.unprocess_tiles(tiles,dir)

        return score

    def __str__(self) -> str:
        NUM_SPACES = 7
        print_str = "\n+-------+-------+-------+-------+"
        for row in self.tiles:
            print_str += "\n|       |       |       |       |"
            print_str += "\n|"
            for tile in row:
                if not tile:
                    print_str += (" " * NUM_SPACES)
                else:
                    num_dig = math.floor(math.log10(tile)) + 1
                    num_st_sp = (NUM_SPACES - num_dig) // 2
                    print_str += (" " * num_st_sp)
                    print_str += str(tile)
                    print_str += (" " * (NUM_SPACES - num_dig - num_st_sp))
                print_str += "|"
            print_str += "\n|       |       |       |       |"
            print_str += "\n+-------+-------+-------+-------+"
        print_str += "\n"
        return print_str
            
