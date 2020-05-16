import math
import random
import copy
from collections import deque
############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):
    # this is equivalent to 64 choose 8
    return math.factorial(n*n)/(math.factorial(n) * math.factorial(n*n - n))

def num_placements_one_per_row(n):
    # using the multiplicative rule of combinatorics, there are n^n solutions (n solutions for each of n rows)
    return n**n

def n_queens_valid(board):
    positions_prev = {}  # dictionary of positions of queens in previous rows in board (col is key for efficiency)
    for row, col in enumerate(board):
        if col in positions_prev.keys():
            return False
        else:
            for col_prev, row_prev in positions_prev.items():
                if abs(col_prev - col) == abs(row_prev - row):
                    return False
            positions_prev[col] = row
    return True


def n_queens_solutions(n):
    board = []
    visited = set()
    frontier = deque()
    frontier.append(board)
    while frontier:
        temp = frontier[-1]
        valid_board = False
        for col in range(n):
            copy_board = copy.copy(temp)
            copy_board.append(col)
            if tuple(copy_board) not in visited:
                if n_queens_valid(copy_board):
                    if len(copy_board) == n:
                        visited.add(tuple(copy_board))
                        yield copy_board
                    else:
                        valid_board = True
                        visited.add(tuple(copy_board))
                        frontier.append(copy_board)
                        break
        if not valid_board:
            frontier.pop()

############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board
        self.row_dim = len(board)
        if self.row_dim != 0:
            self.col_dim = len(board[0])
        else:
            self.col_dim = 0

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        if (row < 0 or row > self.row_dim) or (col < 0 or col > self.col_dim):
            return "Error. Invalid move."
        self.board[row][col] = not self.board[row][col]
        if row - 1 >= 0:
            self.board[row - 1][col] = not self.board[row - 1][col]
        if row + 1 < self.row_dim:
            self.board[row + 1][col] = not self.board[row + 1][col]
        if col - 1 >= 0:
            self.board[row][col - 1] = not self.board[row][col - 1]
        if col + 1 < self.col_dim:
            self.board[row][col + 1] = not self.board[row][col + 1]

    def scramble(self):
        for row in range(self.row_dim):
            for col in range(self.col_dim):
                if random.random() < .5:
                    self.perform_move(row, col)

    def is_solved(self):
        if self.board == [[False for col in range(self.col_dim)] for row in range(self.row_dim)]:
            return True
        return False

    def copy(self):
        return LightsOutPuzzle(copy.deepcopy(self.board))

    def successors(self):
        for row in range(self.row_dim):
            for col in range(self.col_dim):
                copy_board = self.copy()
                copy_board.perform_move(row, col)
                yield (row, col), copy_board

    def find_solution(self):
        frontier = deque()
        frontier.append(self)
        visited = {}
        path = []
        if self.is_solved():
            return path
        while frontier:
            current_puzzle = frontier.popleft()
            for move, new_puzzle in current_puzzle.successors():
                board = tuple(tuple(element) for element in new_puzzle.board)
                if board not in visited:
                    visited[board] = move
                    frontier.append(new_puzzle)
                if new_puzzle.is_solved():
                    while new_puzzle.board != self.board:
                        board = tuple(tuple(element) for element in new_puzzle.board)
                        path.append(visited[board])
                        new_puzzle.perform_move(visited[board][0], visited[board][1])
                    return list(reversed(path))

def create_puzzle(rows, cols):
    board = [[False for col in range(cols)] for row in range(rows)]
    return LightsOutPuzzle(board)

############################################################
# Section 3: Linear Disk Movement
############################################################

# we use the same template from the last problem with new data structures and function implementations
class LinearDiskPuzzle(object):

    def __init__(self, n, length, grid):
        self.n = n
        self.length = length
        self.grid = grid

    def get_grid(self):
        return self.grid

    def copy(self):
        grid = self.grid[:]
        return LinearDiskPuzzle(self.n, self.length, grid)

    def perform_move(self, pos, movement):
        if pos < 0:
            return
        if (pos + movement) >= self.length:
            return
        self.grid[pos], self.grid[pos + movement] = None, self.grid[pos]

    def successors(self):
        for cell in range(self.length):
            if self.grid[cell] is not None:
                if cell + 1 < self.length:
                    if self.grid[cell + 1] is None:
                        copy_grid = self.copy()
                        copy_grid.perform_move(cell, 1)
                        yield ((cell, cell + 1), copy_grid)
                if cell + 2 < self.length:
                    if self.grid[cell + 2] is None and self.grid[cell + 1] is not None:
                        copy_grid = self.copy()
                        copy_grid.perform_move(cell, 2)
                        yield ((cell, cell + 2), copy_grid)

    def successors_distinct(self):
        for cell in range(self.length):
            if self.grid[cell] is not None:
                if cell + 1 < self.length:
                    if self.grid[cell + 1] is None:
                        copy_grid = self.copy()
                        copy_grid.perform_move(cell, 1)
                        yield ((cell, cell + 1), copy_grid)
                if cell + 2 < self.length:
                    if self.grid[cell + 2] is None and self.grid[cell + 1] is not None:
                        copy_grid = self.copy()
                        copy_grid.perform_move(cell, 2)
                        yield ((cell, cell + 2), copy_grid)
                if cell - 1 >= 0:
                    if self.grid[cell - 1] is None:
                        copy_grid = self.copy()
                        copy_grid.perform_move(cell, -1)
                        yield ((cell, cell - 1), copy_grid)
                if cell - 2 >= 0:
                    if self.grid[cell - 2] is None and self.grid[cell - 1] is not None:
                        copy_grid = self.copy()
                        copy_grid.perform_move(cell, -2)
                        yield ((cell, cell - 2), copy_grid)

    def is_solved_identical(self):
        for cell in range(self.length - self.n):
            if self.grid[cell] is not None:
                return False
        return True

    def is_solved_distinct(self):
        for cell in range(self.length - self.n):
            if self.grid[cell] is not None:
                return False
        for cell in range(self.length - self.n, self.length):
            if self.grid[cell] != self.length - cell:
                return False
        return True

    def solve_identical(self):
        frontier = deque()
        frontier.append(self)
        visited = {}
        vis = set()
        path = []
        if self.is_solved_identical():
            return path
        while len(frontier) != 0:
            current_linear_disk = frontier.popleft()
            for move, new_linear_disk in current_linear_disk.successors():
                if tuple(new_linear_disk.grid) not in vis:
                    visited[new_linear_disk] = (move, current_linear_disk)
                    if new_linear_disk.is_solved_identical() is True:
                        while new_linear_disk != self:
                            path.append(visited[new_linear_disk][0])
                            new_linear_disk = visited[new_linear_disk][1]
                        return list(reversed(path))
                    vis.add(tuple(new_linear_disk.grid))
                    frontier.append(new_linear_disk)

    def solve_distinct(self):
        frontier = deque()
        frontier.append(self)
        visited = {}
        vis = set()
        path = []
        if self.is_solved_distinct():
            return path
        while frontier:
            current_linear_disk = frontier.popleft()
            for move, new_linear_disk in current_linear_disk.successors_distinct():
                if tuple(new_linear_disk.grid) not in vis:
                    visited[new_linear_disk] = (move, current_linear_disk)
                    if new_linear_disk.is_solved_distinct():
                        while new_linear_disk != self:
                            path.append(visited[new_linear_disk][0])
                            new_linear_disk = visited[new_linear_disk][1]
                        return list(reversed(path))
                    vis.add(tuple(new_linear_disk.grid))
                    frontier.append(new_linear_disk)


def solve_identical_disks(length, n):
    grid = [None if cell >= n else 1 for cell in range(length)]
    puzzle = LinearDiskPuzzle(n, length, grid)
    return puzzle.solve_identical()

def solve_distinct_disks(length, n):
    grid = [None if cell >= n else cell + 1 for cell in range(length)]
    puzzle = LinearDiskPuzzle(n, length, grid)
    return puzzle.solve_distinct()
