import unittest
from board import Board

class test_board_init(unittest.TestCase):

    def test_board_constructor(self):
        bd = Board()

        self.assertEqual(len(bd.tiles),bd.DIM,f'number of rows is {len(bd.tiles)} instead of {bd.DIM}')
        self.assertEqual(len(bd.tiles[0]),bd.DIM,f'number of cols is {len(bd.tiles[0])} instead of {bd.DIM}')
        num_init_tiles = sum(sum(r) for r in [[1 if t != 0 else 0 for t in row] for row in bd.tiles])
        self.assertEqual(num_init_tiles,2,f'number of initialized tiles is {num_init_tiles} instead of 2')

class test_board_move(unittest.TestCase):

    def test_move_up_c0_2000(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][0] = 2
        bd.move("W")
        self.assertEqual(bd.tiles,[[2,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])

    def test_move_up_c0_0020(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[2][0] = 2
        bd.move("W")
        self.assertEqual(bd.tiles,[[2,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])

    def test_move_up_c1_0004(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[3][1] = 4
        bd.move("W")
        self.assertEqual(bd.tiles,[[0,4,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])

    def test_move_up_c0_0240(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[1][0] = 2
        bd.tiles[2][0] = 4
        bd.move("W")
        self.assertEqual(bd.tiles,[[2,0,0,0],[4,0,0,0],[0,0,0,0],[0,0,0,0]])

    def test_move_up_c0_0204(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[1][0] = 2
        bd.tiles[3][0] = 4
        bd.move("W")
        self.assertEqual(bd.tiles,[[2,0,0,0],[4,0,0,0],[0,0,0,0],[0,0,0,0]])
    
    def test_move_up_c0_2004(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][0] = 2
        bd.tiles[3][0] = 4
        bd.move("W")
        self.assertEqual(bd.tiles,[[2,0,0,0],[4,0,0,0],[0,0,0,0],[0,0,0,0]])
   
    def test_move_up_c0_0220_merge(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[1][0] = 2
        bd.tiles[2][0] = 2
        bd.move("W")
        self.assertEqual(bd.tiles,[[4,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
    
    def test_move_up_c0_0202_merge(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[1][0] = 2
        bd.tiles[3][0] = 2
        bd.move("W")
        self.assertEqual(bd.tiles,[[4,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])

    def test_move_up_c0_0404_merge(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[1][0] = 4
        bd.tiles[3][0] = 4
        bd.move("W")
        self.assertEqual(bd.tiles,[[8,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])

    def test_move_up_c3_0404_merge(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[1][3] = 4
        bd.tiles[3][3] = 4
        bd.move("W")
        self.assertEqual(bd.tiles,[[0,0,0,8],[0,0,0,0],[0,0,0,0],[0,0,0,0]])

    def test_move_up_c2_2420(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][2] = 2
        bd.tiles[1][2] = 4
        bd.tiles[2][2] = 2
        bd.move("W")
        self.assertEqual(bd.tiles,[[0,0,2,0],[0,0,4,0],[0,0,2,0],[0,0,0,0]])

    def test_move_up_c2_2220_merge(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][2] = 2
        bd.tiles[1][2] = 2
        bd.tiles[2][2] = 2
        bd.move("W")
        self.assertEqual(bd.tiles,[[0,0,4,0],[0,0,2,0],[0,0,0,0],[0,0,0,0]])

    def test_move_up_c2_0222_merge(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[1][2] = 2
        bd.tiles[2][2] = 2
        bd.tiles[3][2] = 2
        bd.move("W")
        self.assertEqual(bd.tiles,[[0,0,4,0],[0,0,2,0],[0,0,0,0],[0,0,0,0]])

    def test_move_up_c2_2222_merge(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][2] = 2
        bd.tiles[1][2] = 2
        bd.tiles[2][2] = 2
        bd.tiles[3][2] = 2
        bd.move("W")
        self.assertEqual(bd.tiles,[[0,0,4,0],[0,0,4,0],[0,0,0,0],[0,0,0,0]])
    
    def test_move_up_c2_4444_merge(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][2] = 4
        bd.tiles[1][2] = 4
        bd.tiles[2][2] = 4
        bd.tiles[3][2] = 4
        bd.move("W")
        self.assertEqual(bd.tiles,[[0,0,8,0],[0,0,8,0],[0,0,0,0],[0,0,0,0]])

    def test_move_up_c2_8844_merge(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][2] = 8
        bd.tiles[1][2] = 8
        bd.tiles[2][2] = 4
        bd.tiles[3][2] = 4
        bd.move("W")
        self.assertEqual(bd.tiles,[[0,0,16,0],[0,0,8,0],[0,0,0,0],[0,0,0,0]])

    def test_move_lt_r0_2000(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][0] = 2
        bd.move("A")
        self.assertEqual(bd.tiles,[[2,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])

    def test_move_lt_r2_0020(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[2][0] = 2
        bd.move("A")
        self.assertEqual(bd.tiles,[[0,0,0,0],[0,0,0,0],[2,0,0,0],[0,0,0,0]])

    def test_move_lt_r3_0004(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[3][3] = 4
        bd.move("A")
        self.assertEqual(bd.tiles,[[0,0,0,0],[0,0,0,0],[0,0,0,0],[4,0,0,0]])

    def test_move_lt_r0_0240(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][1] = 2
        bd.tiles[0][2] = 4
        bd.move("A")
        self.assertEqual(bd.tiles,[[2,4,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])

    def test_move_lt_r0_0204(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][1] = 2
        bd.tiles[0][3] = 4
        bd.move("A")
        self.assertEqual(bd.tiles,[[2,4,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
    
    def test_move_lt_r0_2004(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][0] = 2
        bd.tiles[0][3] = 4
        bd.move("A")
        self.assertEqual(bd.tiles,[[2,4,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
   
    def test_move_lt_r0_0220_merge(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][1] = 2
        bd.tiles[0][2] = 2
        bd.move("A")
        self.assertEqual(bd.tiles,[[4,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
    
    def test_move_lt_r0_0202_merge(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][1] = 2
        bd.tiles[0][3] = 2
        bd.move("A")
        self.assertEqual(bd.tiles,[[4,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])

    def test_move_lt_c0_0404_merge(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][1] = 4
        bd.tiles[0][3] = 4
        bd.move("A")
        self.assertEqual(bd.tiles,[[8,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])

    def test_move_lt_r3_0404_merge(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[3][1] = 4
        bd.tiles[3][3] = 4
        bd.move("A")
        self.assertEqual(bd.tiles,[[0,0,0,0],[0,0,0,0],[0,0,0,0],[8,0,0,0]])

    def test_move_lt_r2_2420(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[2][0] = 2
        bd.tiles[2][1] = 4
        bd.tiles[2][2] = 2
        bd.move("A")
        self.assertEqual(bd.tiles,[[0,0,0,0],[0,0,0,0],[2,4,2,0],[0,0,0,0]])

    def test_move_lt_r2_2220_merge(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[2][0] = 2
        bd.tiles[2][1] = 2
        bd.tiles[2][2] = 2
        bd.move("A")
        self.assertEqual(bd.tiles,[[0,0,0,0],[0,0,0,0],[4,2,0,0],[0,0,0,0]])

    def test_move_lt_r2_0222_merge(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[2][1] = 2
        bd.tiles[2][2] = 2
        bd.tiles[2][3] = 2
        bd.move("A")
        self.assertEqual(bd.tiles,[[0,0,0,0],[0,0,0,0],[4,2,0,0],[0,0,0,0]])

    def test_move_lt_r2_2222_merge(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[2][0] = 2
        bd.tiles[2][1] = 2
        bd.tiles[2][2] = 2
        bd.tiles[2][3] = 2
        bd.move("A")
        self.assertEqual(bd.tiles,[[0,0,0,0],[0,0,0,0],[4,4,0,0],[0,0,0,0]])
    
    def test_move_lt_r2_4444_merge(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[2][0] = 4
        bd.tiles[2][1] = 4
        bd.tiles[2][2] = 4
        bd.tiles[2][3] = 4
        bd.move("A")
        self.assertEqual(bd.tiles,[[0,0,0,0],[0,0,0,0],[8,8,0,0],[0,0,0,0]])

    def test_move_lt_r2_8844_merge(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[2][0] = 8
        bd.tiles[2][1] = 8
        bd.tiles[2][2] = 4
        bd.tiles[2][3] = 4
        bd.move("A")
        self.assertEqual(bd.tiles,[[0,0,0,0],[0,0,0,0],[16,8,0,0],[0,0,0,0]])

    def test_move_rt_r0_2000(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][0] = 2
        bd.move("D")
        self.assertEqual(bd.tiles,[[0,0,0,2],[0,0,0,0],[0,0,0,0],[0,0,0,0]])

    def test_move_rt_r0_2040(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][0] = 2
        bd.tiles[0][2] = 4
        bd.move("D")
        self.assertEqual(bd.tiles,[[0,0,2,4],[0,0,0,0],[0,0,0,0],[0,0,0,0]])

    def test_move_rt_r0_4040_merge(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][0] = 4
        bd.tiles[0][2] = 4
        bd.move("D")
        self.assertEqual(bd.tiles,[[0,0,0,8],[0,0,0,0],[0,0,0,0],[0,0,0,0]])

    def test_move_rt_r0_4440_merge(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][0] = 4
        bd.tiles[0][1] = 4
        bd.tiles[0][2] = 4
        bd.move("D")
        self.assertEqual(bd.tiles,[[0,0,4,8],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
        
    def test_move_rt_r2_4444_merge(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[2][0] = 4
        bd.tiles[2][1] = 4
        bd.tiles[2][2] = 4
        bd.tiles[2][3] = 4
        bd.move("D")
        self.assertEqual(bd.tiles,[[0,0,0,0],[0,0,0,0],[0,0,8,8],[0,0,0,0]])

    def test_move_dn_c0_2000(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][0] = 2
        bd.move("S")
        self.assertEqual(bd.tiles,[[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,0,0,0]])

    def test_move_dn_c0_2040(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][0] = 2
        bd.tiles[2][0] = 4
        bd.move("S")
        self.assertEqual(bd.tiles,[[0,0,0,0],[0,0,0,0],[2,0,0,0],[4,0,0,0]])

    def test_move_dn_c0_4040_merge(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][0] = 4
        bd.tiles[2][0] = 4
        bd.move("S")
        self.assertEqual(bd.tiles,[[0,0,0,0],[0,0,0,0],[0,0,0,0],[8,0,0,0]])

    def test_move_dn_c0_4440_merge(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][0] = 4
        bd.tiles[1][0] = 4
        bd.tiles[2][0] = 4
        bd.move("S")
        self.assertEqual(bd.tiles,[[0,0,0,0],[0,0,0,0],[4,0,0,0],[8,0,0,0]])
        
    def test_move_dn_c2_4444_merge(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][2] = 4
        bd.tiles[1][2] = 4
        bd.tiles[2][2] = 4
        bd.tiles[3][2] = 4
        bd.move("S")
        self.assertEqual(bd.tiles,[[0,0,0,0],[0,0,0,0],[0,0,8,0],[0,0,8,0]])

def reset_board(bd: Board):
    for r,row in enumerate(bd.tiles):
        for c,tile in enumerate(row):
            if tile:
                bd.tiles[r][c] = 0

if __name__ == "__main__":
    unittest.main()
