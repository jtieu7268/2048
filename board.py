from tile import Tile
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
    """

    DIM = 4
    START_VALS = [2,4]
    START_VALS_WEIGHTS = [0.9,0.1]

    def __init__(self):
        
        self.tiles = [[None] * self.DIM for _ in range(self.DIM)]
        
        # generate first two tiles
        self.new_tile()
        self.new_tile()

    def new_tile(self) -> Tile:
        """generates a new tile with a start value at an open location on the board

        returns
        -------
            Tile : the new tile
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
        
        self.tiles[r][c] = Tile(new_value())
        
        return self.tiles[r][c]
    
    def __str__(self) -> str:
        print_str = "\n+---+---+---+---+"
        for row in self.tiles:
            print_str += "\n| "
            print_str += " | ".join([str(tile) if tile else " " for tile in row])
            print_str += " |"
            print_str += "\n+---+---+---+---+"
        print_str += "\n"
        return print_str
            
