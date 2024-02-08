import unittest
from graphics import Maze, Point
import random

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        for i in range(20000):
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            start_point = Point(random.randint(1, 1000), random.randint(1, 1000))
            num_rows = random.randint(1, 40)
            num_cols = random.randint(1, 40)
            width = random.randint(1, 1000)
            height = random.randint(1, 1000)
            test_maze = Maze(start_point, num_rows, num_cols, width, height)
            print(test_maze.num_cols, test_maze.num_rows)
            self.assertEqual(len(test_maze._cells), num_cols)
            self.assertEqual(len(test_maze._cells[0]), num_rows)
            self.assertEqual(test_maze._cells[0][0].has_top, False)
            self.assertEqual(test_maze._cells[test_maze.num_cols-1][test_maze.num_rows-1].has_bottom, False)
            self.assertEqual(test_maze.solve(), True)

if __name__ == "__main__":
    print("Testing...")
    unittest.main()
