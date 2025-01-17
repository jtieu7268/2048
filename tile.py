class Tile:
    # values = 

    def __init__(self,val):
        self.val = val
        #self.loc = loc
    
    def change_loc(self,r,c):
        self.loc = (r,c)

    def __str__(self):
        return str(self.val)