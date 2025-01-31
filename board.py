from enum import Enum
from random import choice
from collections import deque
import math

class BoardStatus(Enum):
    PLAYING = 0
    WIN = 1
    GAMEOVER = 2

class Move(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class Board:
    """board for playing 2048.

    Attributes
    ----------
    tiles : list[list[Board]]
        the tiles of the board represented as a 2d array
    
    DIM : int
        the dimension of each side of the board
    
    START_VALS : list[int]
        a list of possible values for new tiles on the board
    
    WIN_VAL : int
        the value of the tile to form to win
    
    Methods
    -------
    transpose(tiles: list[list[int]]) -> list[list[int]]
        returns a copy of tiles transposed
    
    reverse(tiles: list[list[int]]) -> list[list[int]]
        returns a copy of tiles reversed left to right
    
    process_tiles(dir: Move) -> list[list[int]]
        processes board tiles based on direction dir so move related methods can be applied generally independent of direction
    
    unprocess_tiles(tiles: list, dir: Move) -> list[list[int]]
        unprocesses tiles based on direction dir to restore tiles into original board tiles orientation
    
    is_valid_move(dir: Move) -> bool
        returns whether moving tiles in direction dir results in a change in the board tiles    
    
    new_tile()
        generates a new tile with a start value at an open location on the board
    
    move(dir: Move) -> int
        modifies board tiles according to direction dir, returns score from move
    
    is_end()
        returns status of the board tiles
    """

    DIM = 4
    START_VALS = [2] * 9 + [4] # 90% prob of 2, 10% prob of 1

    def __init__(self, win_val: int = 2048):
        
        self.tiles = [[0] * self.DIM for _ in range(self.DIM)]
        self.WIN_VAL = win_val
        
        # generate first two tiles
        self.new_tile()
        self.new_tile()
    
    def transpose(tiles: list[list[int]]) -> list[list[int]]:
        """transposes a copy of tiles and returns.

        Parameters
        ----------
        tiles : list
            2d array representing current board tiles

        Returns
        -------
        list
            copy of tiles transposed
        """

        return list(map(list,zip(*tiles)))
        
    def reverse(tiles: list[list[int]]) -> list[list[int]]:
        """reverses a copy of tiles from left to right

        Parameters
        ----------
        tiles : list
            2d array representing current board tiles
        
        Returns
        -------
        list
            copy of tiles reversed left to right

        """

        return [vector[::-1] for vector in tiles]

    def process_tiles(self, dir: Move) -> list[list[int]]:
        """processes board tiles based on direction dir so move-related methods can be applied generally independent of direction.

        Parameters
        ----------
        dir : Move
            represents direction of move

        Returns
        -------
        list
            a copy of board tiles transposed and/or reversed based on dir
        """

        tiles = self.tiles
        if dir == Move.UP or dir == Move.DOWN:
            tiles = Board.transpose(tiles)
        if dir == Move.RIGHT or dir == Move.DOWN:
            tiles = Board.reverse(tiles)
        return tiles

    def unprocess_tiles(self, tiles: list[list[int]], dir: Move) -> list[list[int]]:
        """unprocesses tiles based on direction dir to restore tiles into original board tiles orientation.

        Parameters
        ----------
        tiles : list
            the previously processed board tiles
        
        dir : Move
            the direction of the move upon which the previous processing was based

        Returns
        -------
        list
            a copy of tiles transposed and/or reversed to undo previous processing based on dir
        """

        if dir == Move.RIGHT or dir == Move.DOWN:
            tiles = Board.reverse(tiles)
        if dir == Move.UP or dir == Move.DOWN:
            tiles = Board.transpose(tiles)
        return tiles

    def is_valid_move(self, dir: Move) -> bool:
        """checks that move is valid, i.e., moving tiles yields a change to board tiles.

        Parameters
        ----------
        dir : Move
            direction of the move to be applied to board tiles

        Returns
        -------
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
        """generates a new tile with a start value at an open location on the board.

        directly modifies board tiles
        """
        
        # generate random position from open positions on the board
        open_loc = [(i,j) for i in range(self.DIM) for j in range(self.DIM) if self.tiles[i][j] == 0]
        if open_loc:
            r,c = choice(open_loc)

            # generate random value from start values
            self.tiles[r][c] = choice(self.START_VALS)

    def move(self,dir: Move) -> int:
        """modifies board tiles according to direction dir.

        tiles slide in chosen direction based on the following:
	        1. tiles slide until stopped by edge of board
	        2. if two tiles of the same number collide, they merge to form a tile with the value of their sum
	        3. if three tiles with the same value collide, only the two farthest into the chosen direction merge
	        4. if four tiles with the same value collide, the first two and the last two merge

        Parameters
        ----------
        dir : Move
            the direction to move tiles

        Returns
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

    def is_end(self, won: bool=False) -> BoardStatus:
        """returns status of the board tiles.

        if board is playable, returns BoardStatus.PLAYING or returns BoardStatus.WIN if board tiles contains WIN_VAL
        if game is over, returns BoardStatus.GAMEOVER (there are no legal moves)
        
        Paramaters
        ----------
        won : bool
            boolean indicating whether game has been won i.e. if tile with WIN_VAL has been created
        
        Returns
        -------
        BoardStatus
            the status of the game, BoardStatus.PLAYING if game is not over, BoardStatus.WIN if board contains WIN_VAL, BoardStatus.GAMEOVER if there are no legal moves
        """

        def is_in_board(val: int):
            return any(val in row for row in self.tiles)
        
        def got_win_val():
            return is_in_board(self.WIN_VAL)
            
        def no_legal_moves():
            # checks if board is filled
            if is_in_board(0): 
                return False
            # board is filled, checks if there are possible merges
            else:
                for orientation in [self.tiles,self.process_tiles(Move.UP)]:
                    for vector in orientation:
                        prev_val_pos = -1
                        for i,tile in enumerate(vector):
                            if prev_val_pos != -1 and tile == vector[prev_val_pos]:
                                return False
                            prev_val_pos = i
                return True
                            
        if not won and got_win_val(): return BoardStatus.WIN
        if no_legal_moves(): return BoardStatus.GAMEOVER
        return BoardStatus.PLAYING

    def play_round(self, dir: Move, won: bool) -> tuple[int, BoardStatus]:
        """executes a round of 2048 including moving bd in direction dir, assuming valid move, generates next tile if possible, returns score from move and state of board.

        Parameters
        ----------
        dir : Move
            the direction to move tiles
            
        won : bool
            boolean indicating whether game has been won i.e. if tile with WIN_VAL has been created

        Returns
        -------
        int
            the sum of all the merged tiles resulting from moving tiles in direction dir

        BoardStatus
            the status of the game, BoardStatus.PLAYING if game is not over, BoardStatus.WIN if board contains WIN_VAL, BoardStatus.GAMEOVER if there are no legal moves
        """

        score = self.move(dir)
        self.new_tile()
        state = self.is_end(won)
        return score, state

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
            
