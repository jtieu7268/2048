import unittest
from board import Board

class test_board(unittest.TestCase):
    def test_board_constructor(self):
        bd = Board()

        self.assertEqual(len(bd.tiles),bd.DIM,f'number of rows is {len(bd.tiles)} instead of {bd.DIM}')
        self.assertEqual(len(bd.tiles[0]),bd.DIM,f'number of cols is {len(bd.tiles[0])} instead of {bd.DIM}')
        num_init_tiles = sum(sum(r) for r in [[1 if t != None else 0 for t in row] for row in bd.tiles])
        self.assertEqual(num_init_tiles,2,f'number of initialized tiles is {num_init_tiles} instead of 2')

if __name__ == "__main__":
    unittest.main()
