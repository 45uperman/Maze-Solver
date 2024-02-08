from tkinter import Tk, BOTH, Canvas
from time import sleep
import random

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__root.title = "Maze Solver"
        self.canvas = Canvas(self.__root, {"width": width, "height": height, "background": "#d9d9d9"})
        self.canvas.pack(fill= BOTH, expand= 1)
        self.running = False
    
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()
    
    def close(self):
        self.running = False
    
    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point_a, point_b):
        self.a = point_a
        self.b = point_b
    
    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.a.x, self.a.y, self.b.x, self.b.y, fill=fill_color, width=2
        )
        canvas.pack()

class Cell:
    def __init__(self, window=None, corners=(Point(0, 0), Point(1, 1)), color="black", has_top=True, has_right=True, has_bottom=True, has_left=True):
        self._window = window
        self._corners = self.get_corners(corners)
        self._width = abs(self._corners[0].x - self._corners[2].x)
        self._height = abs(self._corners[0].y - self._corners[2].y)
        self.color = color
        self.has_top = has_top
        self.has_right = has_right
        self.has_bottom = has_bottom
        self.has_left = has_left
        self.visited = False
    
    def draw_path(self, to_cell, undo=False):
        if undo:
            color = "gray"
        else:
            color = "red"
        try:
            self._window.draw_line(Line(self.get_center(), to_cell.get_center()), color)
        except AttributeError:
                if self._window is not None:
                    raise AttributeError(f"'{type(self.window)}' object is not a window!")
    
    def draw(self):
        try:
            if self.has_top:
                self._window.draw_line(Line(self._corners[0], self._corners[1]), self.color)
            else:
                self._window.draw_line(Line(self._corners[0], self._corners[1]), "#d9d9d9")
            if self.has_right:
                self._window.draw_line(Line(self._corners[1], self._corners[2]), self.color)
            else:
                self._window.draw_line(Line(self._corners[1], self._corners[2]), "#d9d9d9")
            if self.has_bottom:
                self._window.draw_line(Line(self._corners[2], self._corners[3]), self.color)
            else:
                self._window.draw_line(Line(self._corners[2], self._corners[3]), "#d9d9d9")
            if self.has_left:
                self._window.draw_line(Line(self._corners[3], self._corners[0]), self.color)
            else:
                self._window.draw_line(Line(self._corners[3], self._corners[0]), "#d9d9d9")
        except AttributeError:
                if self.window is not None:
                    raise AttributeError(f"'{type(self.window)}' object is not a window!")
    
    def get_center(self):
        return Point(self._corners[0].x + (self._width / 2), self._corners[0].y + (self._height / 2))
    
    def get_corners(self, corners=None):
        if corners is None:
            return self._corners
        else:
            top_left = Point(min(corners[0].x, corners[1].x), min(corners[0].y, corners[1].y))
            bottom_right = Point(max(corners[0].x, corners[1].x), max(corners[0].y, corners[1].y))
            return (top_left, Point(bottom_right.x, top_left.y), bottom_right, Point(top_left.x, bottom_right.y))
    
    def connect(self, other, direction):
        if direction == "up":
            self.has_top = False
            other.has_bottom = False
        elif direction == "right":
            self.has_right = False
            other.has_left = False
        elif direction == "down":
            self.has_bottom = False
            other.has_top = False
        elif direction == "left":
            self.has_left = False
            other.has_right = False

class Maze:
    def __init__(self, start, num_rows, num_cols, cell_width, cell_height, window=None):
        self.start = start
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.window = window
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r()
        self._reset_visited_flags()
        self._end = self._cells[self.num_cols-1][self.num_rows-1]
    
    def _create_cells(self):
        self._cells = []
        for i in range(self.num_cols):
            column = []
            for j in range(self.num_rows):
                next = Cell(
                    self.window, 
                    (Point(self.start.x + (self.cell_width * i), self.start.y + (self.cell_height * j)), 
                     Point(self.start.x + self.cell_width + (self.cell_width * i), self.start.y + self.cell_height + (self.cell_height * j)))
                     )
                column.append(next)
                try:
                    next.draw()
                    self._animate(0.01)
                except AttributeError:
                    if self.window is not None:
                        raise AttributeError(f"'{type(self.window)}' object is not a window!")
            self._cells.append(column)
    
    def _draw_cell(self, cell):
        try:
            cell.draw()
        except AttributeError:
            if self.window is not None:
                raise AttributeError(f"'{type(self.window)}' object is not a window!")
    
    def _animate(self, time=0.05):
        self.window.redraw()
        sleep(time)
    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top = False
        self._draw_cell(self._cells[0][0])
        self._cells[self.num_cols-1][self.num_rows-1].has_bottom = False
        self._draw_cell(self._cells[self.num_cols-1][self.num_rows-1])

    def _break_walls_r(self, i=0, j=0):
        self._cells[i][j].visited = True
        while True:
            to_visit = []
            if self._cells[i][j-1].visited is False and j > 0:
                    to_visit.append((i, j-1, "up"))
            try:
                if self._cells[i+1][j].visited is False:
                    to_visit.append((i+1, j, "right"))
            except IndexError:
                pass
            try:
                if self._cells[i][j+1].visited is False:
                    to_visit.append((i, j+1, "down"))
            except IndexError:
                pass
            if self._cells[i-1][j].visited is False and i > 0:
                    to_visit.append((i-1, j, "left"))
            if not to_visit:
                return
            next = random.choice(to_visit)
            self._cells[i][j].connect(self._cells[next[0]][next[1]], next[2])
            try:
                self._draw_cell(self._cells[i][j])
                self._draw_cell(self._cells[next[0]][next[1]])
                self._animate(0.01)
            except AttributeError:
                if self.window is not None:
                    raise AttributeError(f"'{type(self.window)}' object is not a window!")
            self._break_walls_r(next[0], next[1])
    
    def _reset_visited_flags(self):
        for column in self._cells:
            for cell in column:
                cell.visited = False
    
    def solve(self, current_cell=None):
        if current_cell is None:
            current_cell = self._cells[0][0]
        current_cell.visited = True
        found_exit = False
        directions = [current_cell.has_right, current_cell.has_bottom, current_cell.has_left, current_cell.has_top]
        try:
            self._animate()
        except AttributeError:
                if self.window is not None:
                    raise AttributeError(f"'{type(self.window)}' object is not a window!")
        if current_cell == self._end:
            return True
        
        for direction_index in range(len(directions)):
            if directions[direction_index] is False:
                next = self._move(current_cell, direction_index)
                if next is not False and next.visited is False:
                    current_cell.draw_path(next)
                    found_exit = self.solve(next)
                    if found_exit:
                       return True
                    else:
                        current_cell.draw_path(next, True)
        return False
    
    def _move(self, cell, direction):
        top_left = cell.get_corners()[0]
        offsets = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        x, y = ((top_left.x - self.start.x) // self.cell_width) + offsets[direction][0], ((top_left.y - self.start.y) // self.cell_height) + offsets[direction][1]
        print((top_left.x, top_left.y), (x, y), direction)
        try:
            next_cell = self._cells[x][y]
        except IndexError:
            return False
        if next_cell.visited:
            return False
        return next_cell
