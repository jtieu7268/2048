import unittest
from board import Board
import play_2048

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

class test_board_move_score(unittest.TestCase):

    def test_score_merge_0_up(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[1][0] = 2
        bd.tiles[2][2] = 2
        self.assertEqual(bd.move("A"),0)

    def test_score_merge_0_rt(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[1][0] = 2
        bd.tiles[2][2] = 2
        self.assertEqual(bd.move("D"),0)

    def test_score_merge_0_dn(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[1][0] = 2
        bd.tiles[2][2] = 2
        self.assertEqual(bd.move("S"),0)

    def test_score_merge_0_lt(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[1][0] = 2
        bd.tiles[2][2] = 2
        self.assertEqual(bd.move("A"),0)
    
    def test_score_merge_1_up(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[1][0] = 2
        bd.tiles[2][0] = 2
        self.assertEqual(bd.move("W"),4)

    def test_score_merge_1_rt(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[1][0] = 4
        bd.tiles[1][2] = 4
        self.assertEqual(bd.move("D"),8)

    def test_score_merge_1_dn(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[1][0] = 2
        bd.tiles[2][0] = 2
        self.assertEqual(bd.move("S"),4)

    def test_score_merge_1_lt(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[1][0] = 4
        bd.tiles[1][2] = 4
        self.assertEqual(bd.move("A"),8)

    def test_score_merge_2_up_diff_vector(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][0] = 2
        bd.tiles[1][0] = 2
        bd.tiles[0][3] = 4
        bd.tiles[1][3] = 4
        self.assertEqual(bd.move("W"),12)
    
    def test_score_merge_2_up_same_vector(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][0] = 2
        bd.tiles[1][0] = 2
        bd.tiles[2][0] = 4
        bd.tiles[3][0] = 4
        self.assertEqual(bd.move("W"),12)

    def test_score_merge_2_rt_diff_vector(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][0] = 16
        bd.tiles[0][1] = 16
        bd.tiles[3][0] = 64
        bd.tiles[3][1] = 64
        self.assertEqual(bd.move("D"),160)

    def test_score_merge_2_rt_same_vector(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[3][0] = 16
        bd.tiles[3][1] = 16
        bd.tiles[3][2] = 64
        bd.tiles[3][3] = 64
        self.assertEqual(bd.move("D"),160)

    def test_score_merge_2_dn_diff_vector(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][0] = 2
        bd.tiles[1][0] = 2
        bd.tiles[0][3] = 4
        bd.tiles[1][3] = 4
        self.assertEqual(bd.move("S"),12)
    
    def test_score_merge_2_dn_same_vector(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][0] = 2
        bd.tiles[1][0] = 2
        bd.tiles[2][0] = 4
        bd.tiles[3][0] = 4
        self.assertEqual(bd.move("S"),12)

    def test_score_merge_2_lt_diff_vector(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[0][0] = 16
        bd.tiles[0][1] = 16
        bd.tiles[3][0] = 64
        bd.tiles[3][1] = 64
        self.assertEqual(bd.move("A"),160)

    def test_score_merge_2_lt_same_vector(self):
        bd = Board()
        reset_board(bd)
        bd.tiles[3][0] = 16
        bd.tiles[3][1] = 16
        bd.tiles[3][2] = 64
        bd.tiles[3][3] = 64
        self.assertEqual(bd.move("A"),160)

class test_is_valid_move(unittest.TestCase):

    def test_is_valid_move_invalid_dir(self):
        bd = Board()
        bd.tiles = [[0,0,0,0],[0,2,0,0],[0,0,2,0],[0,0,0,0]]
        self.assertEqual(play_2048.is_valid_move(bd,"F"),False)

    def test_is_valid_move_invalid_dir_double_letter(self):
        bd = Board()
        bd.tiles = [[0,0,0,0],[0,2,0,0],[0,0,2,0],[0,0,0,0]]
        self.assertEqual(play_2048.is_valid_move(bd,"WW"),False)

    def test_is_valid_move_valid_up(self):
        bd = Board()
        bd.tiles = [[0,0,0,0],[0,2,0,0],[0,0,2,0],[0,0,0,0]]
        self.assertEqual(play_2048.is_valid_move(bd,"W"),True)

    def test_is_valid_move_valid_rt(self):
        bd = Board()
        bd.tiles = [[0,0,0,0],[0,2,0,0],[0,0,2,0],[0,0,0,0]]
        self.assertEqual(play_2048.is_valid_move(bd,"D"),True)
    
    def test_is_valid_move_valid_dn(self):
        bd = Board()
        bd.tiles = [[0,0,0,0],[0,2,0,0],[0,0,2,0],[0,0,0,0]]
        self.assertEqual(play_2048.is_valid_move(bd,"S"),True)

    def test_is_valid_move_valid_lt(self):
        bd = Board()
        bd.tiles = [[0,0,0,0],[0,2,0,0],[0,0,2,0],[0,0,0,0]]
        self.assertEqual(play_2048.is_valid_move(bd,"A"),True)

    def test_is_valid_move_invalid_up(self):
        bd = Board()
        bd.tiles = [[0,2,2,0],[0,4,0,0],[0,0,0,0],[0,0,0,0]]
        self.assertEqual(play_2048.is_valid_move(bd,"W"),False)

    def test_is_valid_move_invalid_rt(self):
        bd = Board()
        bd.tiles = [[0,0,2,4],[0,0,0,4],[0,0,0,0],[0,0,0,0]]
        self.assertEqual(play_2048.is_valid_move(bd,"D"),False)
    
    def test_is_valid_move_invalid_dn(self):
        bd = Board()
        bd.tiles = [[0,0,0,0],[0,0,0,0],[0,2,0,0],[0,4,2,0]]
        self.assertEqual(play_2048.is_valid_move(bd,"S"),False)

    def test_is_valid_move_invalid_lt(self):
        bd = Board()
        bd.tiles = [[4,2,0,0],[2,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.assertEqual(play_2048.is_valid_move(bd,"W"),False)

class test_game_over_status(unittest.TestCase):
    
    def test_not_game_over_board_vertical_full(self):
        bd = Board()
        reset_board(bd)
        bd.tiles = [[2,4,8,128],[8,4,64,1024],[4,16,128,256],[2,8,16,64]]
        self.assertEqual(play_2048.game_over_status(bd),0)
    
    def test_not_game_over_board_horizontal_full(self):
        bd = Board()
        reset_board(bd)
        bd.tiles = [[2,4,8,128],[8,8,64,1024],[4,16,128,256],[2,8,16,64]]
        self.assertEqual(play_2048.game_over_status(bd),0)

    def test_game_over_board_full(self):
        bd = Board()
        reset_board(bd)
        bd.tiles = [[2,4,8,128],[8,32,64,1024],[128,16,128,256],[2,8,16,64]]
        self.assertEqual(play_2048.game_over_status(bd),2)

    def test_not_game_over_board_not_full(self):
        bd = Board()
        reset_board(bd)
        bd.tiles = [[2,4,8,128],[8,4,64,1024],[4,16,128,256],[0,8,16,64]]
        self.assertEqual(play_2048.game_over_status(bd),0)

    def test_game_over_2048(self):
        bd = Board()
        reset_board(bd)
        bd.tiles = [[0,4,8,128],[0,8,64,2048],[0,0,128,256],[0,8,16,64]]
        self.assertEqual(play_2048.game_over_status(bd),1)

class test_game_loop(unittest.TestCase):

    def test_game_loop_win(self):
        bd = Board()
        bd.tiles[0][0] = 1024
        bd.tiles[1][0] = 1024
        # move up then quit
        play_2048.game_loop()

def reset_board(bd):
    bd.tiles = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

if __name__ == "__main__":
    unittest.main()
