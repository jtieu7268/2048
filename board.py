import random

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

        if dir == "W":
            # check each column
            for c, col in enumerate(zip(*self.tiles)):
                empty_queue = []
                prev_tile_pos = -1
                for r, tile in enumerate(col):
                    # empty tile
                    if not tile:
                        empty_queue.append(r)
                    # tile exists
                    else:
                        # merge
                        if prev_tile_pos != -1 and self.tiles[prev_tile_pos][c] == tile:
                            self.tiles[prev_tile_pos][c] *= 2
                            self.tiles[r][c] = 0
                            empty_queue.append(r)
                            prev_tile_pos = -1
                        else:
                            # move tile to furthest empty space
                            if empty_queue:
                                new_r = empty_queue.pop(0)
                                self.tiles[new_r][c] = tile
                                self.tiles[r][c] = 0
                                empty_queue.append(r)
                            # tile does not move because not further empty spaces and no merging possible
                            prev_tile_pos = r

    def __str__(self) -> str:
        print_str = "\n+---+---+---+---+"
        for row in self.tiles:
            print_str += "\n| "
            print_str += " | ".join([str(tile) if tile else " " for tile in row])
            print_str += " |"
            print_str += "\n+---+---+---+---+"
        print_str += "\n"
        return print_str
            
