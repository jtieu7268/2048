class Tile:
    """ a class representing a tile on 2048 board

    attributes
    ----------
    val : int
        the value of the tile

    methods
    -------
    change_loc(r,c)
        changes the location of the tile on the board to r,c

    """

    def __init__(self,val):
        self.val = val
        #self.loc = loc
    
    def change_loc(self,r,c):
        self.loc = (r,c)

    def __str__(self):
        return str(self.val)