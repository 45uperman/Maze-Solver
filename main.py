from graphics import Window, Point, Maze

def main():
    win = Window(800, 600)
    test_maze = Maze(Point(10, 10), 40, 40, 20, 20, win)
    test_maze.solve()
    win.wait_for_close()

main()
