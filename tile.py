class Tile:
    """ a class representing a tile on 2048 board

    attributes
    ----------
    val : int
        the value of the tile

    methods
    -------
    get_val()
        returns value of the tile
    set_val(new val: int)
        changes value of the tile to new_val
    change_loc(r: int,c: int)
        changes the location of the tile on the board to r,c

    """

    def __init__(self,val: int):
        self.val = val
        #self.loc = loc
    
    def get_val(self):
        return self.val
    
    def set_val(self,val: int):
        self.val = val
    
    def change_loc(self,r: int,c: int):
        self.loc = (r,c)

    def __str__(self):
        return str(self.val)