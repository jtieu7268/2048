import random
import math

class Board:
    """ a class representing board for playing 2048

    attributes
    ----------
    tiles : list
        the tiles of the board represented as a 2d array
    DIM : int
        the dimension of each side of the board
    START_VALS : list
        a list of possible values for new tiles on the board
    START_VALS : list
        a list of the weights representing the likelihood of generating the respective START_VALS

    methods
    -------
    new_tile()
        generates a new tile with a start value at an open location on the board
    move(dir: str)
        modifies board tiles according to direction dir
    """

    DIM = 4
    START_VALS = [2,4]
    START_VALS_WEIGHTS = [0.9,0.1]

    def __init__(self):
        
        self.tiles = [[0] * self.DIM for _ in range(self.DIM)]
        
        # generate first two tiles
        self.new_tile()
        self.new_tile()

    def new_tile(self):
        """generates a new tile with a start value at an open location on the board

            directly modifies board tiles
        """

        # function to generate start value
        def new_value():
            return random.choices(self.START_VALS,self.START_VALS_WEIGHTS)[0]
        
        # generate random position
        r = random.randint(0,self.DIM-1)
        c = random.randint(0,self.DIM-1)
        # keep regenerating position until position is unoccupied 
        while self.tiles[r][c]:
            r = random.randint(0,self.DIM-1)
            c = random.randint(0,self.DIM-1)
        
        self.tiles[r][c] = new_value()
    
    def move(self,dir):
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
        """

        is_horizontal = dir == "A" or dir == "D"
        tiles = self.tiles if is_horizontal else zip(*self.tiles)
        # check each vector in direction of dir
        for i, dir_vector in enumerate(tiles):
            empty_queue = []
            prev_tile_pos = -1
            is_UL = dir == "A" or dir == "W"
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
                            self.tiles[i][j_actual] = 0
                        else:
                            self.tiles[prev_tile_pos][i] *= 2
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
                        # tile does not move because not further empty spaces and no merging possible
                        else:
                            prev_tile_pos = j_actual

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
            
