import random
import copy
from queue import PriorityQueue
from math import sqrt, inf, ceil
import heapq
############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    tile = 1
    board = []
    for row in range(rows):
        board_row = []
        for col in range(cols):
            board_row.append(tile)
            tile += 1
        board.append(board_row)
    board[rows - 1][cols - 1] = 0
    return TilePuzzle(board)

class TilePuzzle(object):
    
    # Required
    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.columns = 0
        self.zero_row = -1
        self.zero_column = -1
        if self.rows:
            self.columns = len(board[0])
            for row in range(len(board)):
                for column in range(len(board[0])):
                    if board[row][column] == 0:
                        self.zero_row = row
                        self.zero_column = column

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        direction = direction.lower()
        if direction in ["up", "down", "left", "right"]:
            if direction == "down":
                if self.zero_row != self.rows - 1:
                    self.board[self.zero_row][self.zero_column], self.board[self.zero_row + 1][self.zero_column] = \
                        self.board[self.zero_row + 1][self.zero_column], self.board[self.zero_row][self.zero_column]
                    self.zero_row += 1
                    return True
            if direction == "up":
                if self.zero_row != 0:
                    self.board[self.zero_row][self.zero_column], self.board[self.zero_row - 1][self.zero_column] = \
                        self.board[self.zero_row - 1][self.zero_column], self.board[self.zero_row][self.zero_column]
                    self.zero_row -= 1
                    return True
            if direction == "left":
                if self.zero_column != 0:
                    self.board[self.zero_row][self.zero_column], self.board[self.zero_row][self.zero_column -1] = \
                        self.board[self.zero_row][self.zero_column - 1], self.board[self.zero_row][self.zero_column]
                    self.zero_column -= 1
                    return True
            if direction == "right":
                if self.zero_column != self.columns - 1:
                    self.board[self.zero_row][self.zero_column], self.board[self.zero_row][self.zero_column + 1] = \
                        self.board[self.zero_row][self.zero_column + 1], self.board[self.zero_row][self.zero_column]
                    self.zero_column += 1
                    return True
        return False

    def scramble(self, num_moves):
        for move in range(num_moves):
            self.perform_move(random.choice(["up", "down", "left", "right"]))

    def is_solved(self):
        tile = 1
        for row in range(self.rows - 1):
            for col in range(self.columns):
                if self.board[row][col] != tile:
                    return False
                tile += 1
        for col in range(self.columns - 1):
            if self.board[self.rows - 1][col] != tile:
                return False
            tile += 1
        if self.board[self.rows - 1][self.columns - 1] != 0:
            return False
        return True

    def copy(self):
        return TilePuzzle(copy.deepcopy(self.board))

    def successors(self):
        for direction in ["up", "down", "left", "right"]:
            copy = self.copy()
            if copy.perform_move(direction):
                yield direction, copy

    def iddfs_helper(self, limit, moves):
        if self.is_solved():
            yield moves
        elif len(moves) < limit:
            for move, new_puzzle in self.successors():
                new_moves = moves + [move]
                yield from new_puzzle.iddfs_helper(limit, new_moves)

    # Required
    def find_solutions_iddfs(self):
        limit = 0
        solution = False
        while not solution:
            if list(self.iddfs_helper(limit, [])):
                for solution in self.iddfs_helper(limit, []):
                    yield solution
                solution = True
            limit += 1

    def positions_solved_puzzle(self):
        tile = 1
        solved_puzzle_positions = {}
        for row in range(self.rows):
            for col in range(self.columns):
                solved_puzzle_positions[tile] = [row, col]
                tile += 1
        solved_puzzle_positions[0] = [self.rows - 1, self.columns - 1]
        return solved_puzzle_positions

    def manhattan_dist(self, solved__puzzle_positions):
        manhattan_dist = 0
        for row in range(self.rows):
            for col in range(self.columns):
                current_tile = self.board[row][col]
                if current_tile != 0:
                    manhattan_dist += abs(row - solved__puzzle_positions[current_tile][0]) \
                                      + abs(col - solved__puzzle_positions[current_tile][1])
        return manhattan_dist

    def __lt__(self, other):
        return True

    # Required
    def find_solution_a_star(self):
        solved_puzzle_positions = self.positions_solved_puzzle()
        visited = set()
        frontier = PriorityQueue()
        frontier.put((0, self, []))
        if self.is_solved():
            return []
        while not frontier.empty():
            current = frontier.get()
            # current_moves = moves.get()
            for move, new_puzzle in current[1].successors():
                board = tuple(tuple(element) for element in new_puzzle.board)
                if board not in visited:
                    visited.add(board)
                    if new_puzzle.is_solved():
                        return current[2] + [move]
                    frontier.put((new_puzzle.manhattan_dist(solved_puzzle_positions) + 1 + current[0], new_puzzle,
                                 current[2] + [move]))


############################################################
# Section 2: Grid Navigation
############################################################

class GridNavigation(object):

    def __init__(self, board, start_location, end_location):
        self.board = tuple(tuple(element) for element in board)
        self.start_location = list(start_location)
        self.end_location = list(end_location)

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        if direction in ["up", "down", "left", "right", "up-left", "up-right", "down-left", "down-right"]:
            if direction == "up" and self.start_location[0] != 0:
                if self.board[self.start_location[0] - 1][self.start_location[1]] is False:
                    self.start_location[0] -= 1
                    return True
            if direction == "down" and self.start_location[0] != len(self.board) - 1:
                if self.board[self.start_location[0] + 1][self.start_location[1]] is False:
                    self.start_location[0] += 1
                    return True
            if direction == "left" and self.start_location[1] != 0:
                if self.board[self.start_location[0]][self.start_location[1] - 1] is False:
                    self.start_location[1] -= 1
                    return True
            if direction == "right" and self.start_location[1] != len(self.board[0]) - 1:
                if self.board[self.start_location[0]][self.start_location[1] + 1] is False:
                    self.start_location[1] += 1
                    return True
            if direction == "up-left" and self.start_location[0] != 0 and self.start_location[1] != 0:
                if self.board[self.start_location[0] - 1][self.start_location[1] - 1] is False:
                    self.start_location[0] -= 1
                    self.start_location[1] -= 1
                    return True
            if direction == "up-right" and self.start_location[0] != 0 and self.start_location[1] != len(self.board[0]) - 1:
                if self.board[self.start_location[0] - 1][self.start_location[1] + 1] is False:
                    self.start_location[0] -= 1
                    self.start_location[1] += 1
                    return True
            if direction == "down-left" and self.start_location[0] != len(self.board) - 1 and self.start_location[1] != 0:
                if self.board[self.start_location[0] + 1][self.start_location[1] - 1] is False:
                    self.start_location[0] += 1
                    self.start_location[1] -= 1
                    return True
            if direction == "down-right" and self.start_location[0] != len(self.board) - 1 and self.start_location[1] != len(self.board[0]) - 1:
                if self.board[self.start_location[0] + 1][self.start_location[1] + 1] is False:
                    self.start_location[0] += 1
                    self.start_location[1] += 1
                    return True
        return False

    def copy(self):
        return GridNavigation(self.board, self.start_location[:], self.end_location)

    def euclidean_distance(self, other):
        return sqrt((self.start_location[0] - other[0])**2 + (self.start_location[1] - other[1])**2)

    def successors(self):
        for direction in ["up", "down", "left", "right", "up-left", "up-right", "down-left", "down-right"]:
            copy = self.copy()
            if copy.perform_move(direction):
                yield tuple(copy.start_location), copy

    def is_solved(self):
        return self.start_location == self.end_location

    def __lt__(self, other):
        return self.euclidean_distance(self.end_location) < other.euclidean_distance(self.end_location)

    def find_path(self):
        end_location = self.end_location
        visited = set()
        frontier = PriorityQueue()
        frontier.put((0, self, [tuple(self.start_location)]))
        if self.is_solved():
            return frontier.get()[2] + [tuple(self.end_location)]
        while not frontier.empty():
            current = frontier.get()
            for move, new_puzzle in current[1].successors():
                start = tuple(new_puzzle.start_location)
                if start not in visited:
                    visited.add(start)
                    if new_puzzle.is_solved():
                        return current[2] + [move]
                    frontier.put((new_puzzle.euclidean_distance(end_location) +
                                  new_puzzle.euclidean_distance(current[1].start_location) + current[0], new_puzzle,
                                  current[2] + [move]))

def find_path(start, goal, scene):
    puzzle = GridNavigation(scene, start, goal)
    return puzzle.find_path()

############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################

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

    def is_solved_distinct(self):
        for cell in range(self.length - self.n):
            if self.grid[cell] is not None:
                return False
        for cell in range(self.length - self.n, self.length):
            if self.grid[cell] != self.length - cell:
                return False
        return True

    def positions_solved_puzzle(self):
        solved_puzzle_positions = {}
        tile = self.n
        for buffer in range(self.n):
            solved_puzzle_positions[tile] = self.length - self.n + buffer
            tile -= 1
        return solved_puzzle_positions

    def heuristic(self, solved__puzzle_positions):
        heuristic = 0
        for element in range(self.length):
            current_tile = self.grid[element]
            if current_tile is not None:
                heuristic += abs(element - solved__puzzle_positions[current_tile])/2
        return heuristic

    def __lt__(self, other):
        return True

    def solve_distinct(self):
        solved_puzzle_positions = self.positions_solved_puzzle()
        visited = set()
        frontier = []
        heapq.heappush(frontier, (0, self, []))
        if self.is_solved_distinct():
            return []
        while frontier:
            current_linear_disk = heapq.heappop(frontier)
            for move, new_linear_disk in current_linear_disk[1].successors_distinct():
                grid = tuple(new_linear_disk.grid)
                if grid not in visited:
                    visited.add(grid)
                    if new_linear_disk.is_solved_distinct():
                        return current_linear_disk[2] + [move]
                    heapq.heappush(frontier, (new_linear_disk.heuristic(solved_puzzle_positions) + 1 +
                                              current_linear_disk[0], new_linear_disk, current_linear_disk[2] + [move]))


def solve_distinct_disks(length, n):
    grid = [None if cell >= n else cell + 1 for cell in range(length)]
    puzzle = LinearDiskPuzzle(n, length, grid)
    solution = puzzle.solve_distinct()
    return solution

############################################################
# Section 4: Dominoes Game
############################################################

def create_dominoes_game(rows, cols):
    return DominoesGame([[False for col in range(cols)] for row in range(rows)])

class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.board = board
        self.row = len(board)
        if board:
            self.column = len(board[0])

    def get_board(self):
        return self.board

    def reset(self):
        self.board = [[False for col in range(self.column)] for row in range(self.row)]

    def is_legal_move(self, row, col, vertical):
        if row >= 0 and col >= 0:
            if vertical:
                if col < self.column and row + 1 < self.row:
                    if self.board[row][col] is False and self.board[row + 1][col] is False:
                        return True
            elif not vertical:
                if row < self.row and col + 1 < self.column:
                    if self.board[row][col] is False and self.board[row][col + 1] is False:
                        return True
        return False

    def legal_moves(self, vertical):
        for row in range(self.row):
            for col in range(self.column):
                if self.is_legal_move(row, col, vertical):
                    yield (row, col)

    def perform_move(self, row, col, vertical):
        if self.is_legal_move(row, col, vertical):
            if vertical:
                self.board[row][col], self.board[row + 1][col] = True, True
            elif not vertical:
                self.board[row][col], self.board[row][col + 1] = True, True

    def game_over(self, vertical):
        for row in range(self.row):
            for col in range(self.column):
                if self.is_legal_move(row, col, vertical):
                    return False
        return True

    def copy(self):
        return DominoesGame(copy.deepcopy(self.board))

    def successors(self, vertical):
        for row in range(self.row):
            for col in range(self.column):
                copy = self.copy()
                if self.is_legal_move(row, col, vertical):
                    copy.perform_move(row, col, vertical)
                    yield (row, col), copy

    def get_random_move(self, vertical):
        row, col = random.choice(list(self.legal_moves(vertical)))
        self.perform_move(row, col, vertical)

    def max_value(self, alpha, beta, vertical, move, num_moves, limit):
        if num_moves == limit:
            return move, len(list(self.legal_moves(vertical))) - len(list(self.legal_moves(not vertical))), 1
        if self.game_over(vertical):
            return move, len(list(self.legal_moves(vertical))) - len(list(self.legal_moves(not vertical))), 1
        v = -inf
        current_move = move
        number_leaf_nodes = 0
        for new_move, new_puzzle in self.successors(vertical):
            move, utility, leaf_nodes = new_puzzle.min_value(alpha, beta, not vertical, new_move, num_moves + 1, limit)
            if utility > v:
                v = utility
                current_move = new_move
            number_leaf_nodes += leaf_nodes
            if v >= beta:
                break
            if v > alpha:
                alpha = v
        return current_move, v, number_leaf_nodes

    def min_value(self, alpha, beta, vertical, initial_move, num_moves, limit):
        if num_moves == limit:
            return initial_move, len(list(self.legal_moves(not vertical))) - len(list(self.legal_moves(vertical))), 1
        if self.game_over(vertical):
            return initial_move, len(list(self.legal_moves(not vertical))) - len(list(self.legal_moves(vertical))), 1
        v = inf
        current_move = initial_move
        number_leaf_nodes = 0
        for new_move, new_puzzle in self.successors(vertical):
            move, utility, leaf_nodes = new_puzzle.max_value(alpha, beta, not vertical, new_move, num_moves + 1, limit)
            if utility < v:
                v = utility
                current_move = new_move
            number_leaf_nodes += leaf_nodes
            if v <= alpha:
                break
            if v < beta:
                beta = v
        return current_move, v, number_leaf_nodes

    # Required
    def get_best_move(self, vertical, limit):
        return self.max_value(-inf, inf, vertical, (), 0, limit)
