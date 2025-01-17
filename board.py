from tile import Tile
import random

class Board:
    DIM = 4
    def __init__(self):
        
        self.tiles = [[None] * self.DIM for i in range(self.DIM)]
        
        # generate random positions for first two tiles
        r1 = random.randint(0,self.DIM-1)
        c1 = random.randint(0,self.DIM-1)
        r2 = random.randint(0,self.DIM-1)
        c2 = random.randint(0,self.DIM-1)
        # keep regenerating second position while first and second positions are the same
        while r1 == r2 and c1 == c2:
            r2 = random.randint(0,self.DIM-1)
            c2 = random.randint(0,self.DIM-1)
        
        # randomly choose  the starting values of the two tiles
        # 90% chance of 2, 10% chance of 4
        self.tiles[r1][c1] = Tile(random.choices([2,4],[0.9,0.1])[0])
        self.tiles[r2][c2] = Tile(random.choices([2,4],[0.9,0.1])[0])
    
    def __str__(self):
        print_str = "\n+---+---+---+---+"
        for row in self.tiles:
            print_str += "\n| "
            print_str += " | ".join([str(tile) if tile else " " for tile in row])
            print_str += " |"
            print_str += "\n+---+---+---+---+"
        print_str += "\n"
        return print_str
            
