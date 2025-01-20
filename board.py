from random import choices, choice
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
    
    methods
    -------
    new_tile()
        generates a new tile with a start value at an open location on the board
    move(dir: str) -> bool
        modifies board tiles according to direction dir, generates new tile if possible
    is_end()
        # TODO: implement and decide if want to separate
    transpose(tiles: list) -> list
        returns a copy of tiles transposed
    reverse(tiles: list) ->
        returns a copy of tiles reversed
    """

    DIM = 4
    START_VALS = [2] * 9 + [4]

    def __init__(self, win_val: int = 2048):
        
        self.tiles = [[0] * self.DIM for _ in range(self.DIM)]
        self.WIN_VAL = win_val
        
        # generate first two tiles
        self.new_tile()
        self.new_tile()

    def new_tile(self):
        """generates a new tile with a start value at an open location on the board

        directly modifies board tiles
        """
        
        # generate random position from open positions on the board
        r,c = choice([(i,j) for i in range(self.DIM) for j in range(self.DIM) if self.tiles[i][j] == 0])

        self.tiles[r][c] = choices(self.START_VALS)[0]
    
    def move(self,dir: str) -> int:
        """modifies board tiles according to direction dir

        tiles slide in chosen direction based on the following:
	        1. tiles slide until stopped by edge of board
	        2. if two tiles of the same number collide, they merge to form a tile with the value of their sum
	        3. if three tiles with the same value collide, only the two farthest into the chosen direction merge
	        4. if four tiles with the same value collide, the first two and the last two merge

        parameters
        ----------
        dir : str
            the direction to move tiles
            "W": UP
            "D": RIGHT
            "S": DOWN
            "A": LEFT

        returns
        -------
        int
            the sum of all the merged tiles resulting from moving tiles in direction dir
        """
        score = 0
        is_horizontal = dir == "A" or dir == "D"
        is_UL = dir == "A" or dir == "W"
        tiles = self.tiles if is_horizontal else zip(*self.tiles)
        # check each vector in direction of dir
        for i, dir_vector in enumerate(tiles):
            empty_queue = []
            prev_tile_pos = -1
            ordered_dir_vector = dir_vector if is_UL else dir_vector[::-1]
            for j, tile in enumerate(ordered_dir_vector):
                j_actual = j if is_UL else self.DIM-j-1
                # empty tile
                if not tile:
                    empty_queue.append(j_actual)
                # tile exists
                else:
                    # merge
                    is_horizontal_merge = is_horizontal and self.tiles[i][prev_tile_pos] == tile
                    is_vertical_merge = not is_horizontal and self.tiles[prev_tile_pos][i] == tile
                    if prev_tile_pos != -1 and (is_horizontal_merge or is_vertical_merge):
                        if is_horizontal_merge:
                            self.tiles[i][prev_tile_pos] *= 2
                            score += self.tiles[i][prev_tile_pos]
                            self.tiles[i][j_actual] = 0
                        else:
                            self.tiles[prev_tile_pos][i] *= 2
                            score += self.tiles[prev_tile_pos][i]
                            self.tiles[j_actual][i] = 0
                        empty_queue.append(j_actual)
                        prev_tile_pos = -1
                    else:
                        # move tile to furthest empty space
                        if empty_queue:
                            new_j = empty_queue.pop(0)
                            if is_horizontal:
                                self.tiles[i][new_j] = tile
                                self.tiles[i][j_actual] = 0
                            else:
                                self.tiles[new_j][i] = tile
                                self.tiles[j_actual][i] = 0
                            empty_queue.append(j_actual)
                            prev_tile_pos = new_j
                        # tile does not move because no further empty spaces and no merging possible
                        else:
                            prev_tile_pos = j_actual
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
            
