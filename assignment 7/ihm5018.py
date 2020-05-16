from copy import deepcopy


############################################################
# Section 1: Sudoku
############################################################

def sudoku_cells():
    cells = []
    for cell1 in range(9):
        for cell2 in range(9):
            cells.append((cell1, cell2))
    return cells

def sudoku_arcs():
    arcs = []
    corner_boxes = [0, 3, 6]

    for row in range(9):
        for start in range(9):
            for end in range(9):
                if start != end:
                    arcs.append(((row, start), (row, end)))

    for col in range(9):
        for start in range(9):
            for end in range(9):
                if ((start, col), (end, col)) not in arcs and start != end:
                    arcs.append(((start, col), (end, col)))

    for corner_row in corner_boxes:
        for corner_col in corner_boxes:
            box = []
            for row in range(corner_row, corner_row + 3):
                for col in range(corner_col, corner_col + 3):
                    box.append((row, col))
            for index in range(len(box)):
                for index2 in range(len(box)):
                    if (box[index], box[index2]) not in arcs and box[index] != box[index2]:
                        arcs.append((box[index], box[index2]))

    return arcs

def read_board(path):
    numbers = list(range(1,10))
    board = {}
    cell1 = 0
    with open(path, 'r') as f:
        for line in f:
            cell2 = 0
            for cell in line.strip():
                if cell.isdigit():
                    board[(cell1, cell2)] = {int(cell)}
                else:
                    board[(cell1, cell2)] = set(numbers)
                cell2 += 1
            cell1 += 1
    return board

class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
        self.board = board

    def get_values(self, cell):
        return self.board[cell]

    def remove_inconsistent_values(self, cell1, cell2):
        if (cell1, cell2) not in Sudoku.ARCS:
            return False
        values1 = self.get_values(cell1)
        values2 = self.get_values(cell2)
        if len(values2) == 1:
            val = list(values2)[0]
            if val in values1:
                values1.remove(val)
                return True
        return False

    def infer_ac3(self):
        queue = Sudoku.ARCS[:]
        while queue:
            cell1, cell2 = queue.pop(0)
            if self.remove_inconsistent_values(cell1, cell2):
                neighbors = []

                # add row neighbors
                row = cell1[0]
                for col in range(9):
                    potential_neighbor = (row, col)
                    if potential_neighbor != cell2 and potential_neighbor != cell1:
                        neighbors.append(potential_neighbor)

                # add column neighbors
                col = cell1[1]
                for row in range(9):
                    potential_neighbor = (row, col)
                    if potential_neighbor != cell2 and potential_neighbor != cell1:
                        neighbors.append(potential_neighbor)

                # add grid neighbors
                corner_boxes = [0, 3, 6]
                row = cell1[0]
                col = cell1[1]
                row_start = corner_boxes[int(row/3)]
                col_start = corner_boxes[int(col/3)]
                for row in range(3):
                    for col in range(3):
                        potential_neighbor = (row_start + row, col_start + col)
                        if potential_neighbor != cell2 and potential_neighbor != cell1 and \
                                potential_neighbor not in neighbors:
                            neighbors.append(potential_neighbor)

                # add neighbors to queue
                for neighbor in neighbors:
                    queue.append((neighbor, cell1))

    def infer_improved(self):
        new_assignment = True
        while new_assignment:
            new_assignment = False
            self.infer_ac3()
            for cell in Sudoku.CELLS:
                if len(self.get_values(cell)) != 1:
                    for value in self.get_values(cell):
                        # add row neighbors
                        row_unique = True
                        row = cell[0]
                        for col in range(9):
                            if col != cell[1]:
                                if value in self.get_values((row, col)):
                                    row_unique = False
                                    break

                        if row_unique:
                            self.board[cell] = {value}
                            new_assignment = True
                            break

                        # add col neighbors
                        col_unique = True
                        col = cell[1]
                        for row in range(9):
                            if row != cell[0]:
                                if value in self.get_values((row, col)):
                                    col_unique = False
                                    break

                        if col_unique:
                            self.board[cell] = {value}
                            new_assignment = True
                            break

                        # add grid neighbors
                        grid_unique = True
                        corner_boxes = [0, 3, 6]
                        row = cell[0]
                        col = cell[1]
                        row_start = corner_boxes[int(row / 3)]
                        col_start = corner_boxes[int(col / 3)]
                        for row in range(3):
                            for col in range(3):
                                if (row_start + row, col_start + col) != cell:
                                    if value in self.get_values((row_start + row, col_start + col)):
                                        grid_unique = False
                                        break

                        if grid_unique:
                            self.board[cell] = {value}
                            new_assignment = True
                            break

    def infer_with_guessing(self):
        self.infer_improved()
        new_board, _ = Sudoku.infer_with_guessing_recursive(self)
        self.board = new_board

    @staticmethod
    def infer_with_guessing_recursive(puzzle):
        solved = True
        for cell in Sudoku.CELLS:
            if len(puzzle.board[cell]) != 1:
                solved = False
                break

        if solved:
            return puzzle.board, True

        unassigned_cell = None
        for cell in Sudoku.CELLS:
            if len(puzzle.board[cell]) > 1:
                unassigned_cell = cell
                break

        for value in puzzle.board[unassigned_cell]:
            original_board = deepcopy(puzzle.board)
            puzzle.board[unassigned_cell] = {value}
            puzzle.infer_improved()

            consistent = True
            for cell in Sudoku.CELLS:
                if len(puzzle.board[cell]) == 0:
                    consistent = False
                    break

            if consistent:
                new_board, valid_board = puzzle.infer_with_guessing_recursive(puzzle)
                puzzle.board = new_board
                if valid_board:
                    return puzzle.board, True
            puzzle.board = original_board

        return puzzle.board, False
