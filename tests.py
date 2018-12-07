import unittest
import math
import solver


class TestSudoku(unittest.TestCase):
    def setUp(self):
        super(TestSudoku, self).setUp()
        self.grid = solver.creating_grid('cell_2.txt')
        self.empty_position = solver.find_empty_position(self.grid)

    def test_creating_grid(self):
        for width in self.grid:
            self.assertEquals(len(width), len(self.grid))

    def test_find_empty_position(self):
        r, w = self.empty_position
        self.assertEquals(self.grid[r][w], '.')

    def test_get_row(self):
        row = solver.get_row(self.grid, self.empty_position)
        self.assertIn(row, self.grid)

    def test_get_col(self):
        pos = []
        r, w = self.empty_position
        pos.append([self.grid[i][w] for i in range(len(self.grid[w]))])
        col = solver.get_col(self.grid, self.empty_position)
        self.assertIn(col, pos)

    def test_get_block(self):
        self.assertTrue(int(math.sqrt(len(self.grid))))

    def test_all_solutions(self):
        if len(solver.all_solutions(self.grid)) == 0:
            self.assertEquals(solver.all_solutions(self.grid), "No solutions")

if __name__ == '__main__':
    unittest.main()
