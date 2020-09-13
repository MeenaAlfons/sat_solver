import itertools
from math import sqrt


class SudokuRules:
    """
    Class to help generate the right constraints for our experiments.
    """
    def __init__(self, sudoku_size):
        """
        Initializes rule cnf with standard constraints.
        :param sudoku_size: size of the square sudoku. E.g. size of a 9*9 sudoku is 9.
        """
        self.sudoku_size = sudoku_size
        self.rules_cnf = []
        self.add_standard_constraint()

    def reset(self):
        """
        Resets to standard constraints.
        """
        self.rules_cnf = []
        self.add_standard_constraint()

    def add_standard_constraint(self):
        """
        Creates the constraint which states that each field must have exactly one assignment.
        """
        for row in range(self.sudoku_size):
            for col in range(self.sudoku_size):
                field = str(row+1) + str(col+1)
                curr_vars = [int(field + str(i+1)) for i in range(self.sudoku_size)]

                # at least one value
                self.rules_cnf.append(curr_vars)

                # at most one value
                pairs = list(itertools.combinations(curr_vars, 2))
                pairs = [[-a, -b] for a, b in pairs]
                self.rules_cnf.extend(pairs)

    def add_alldiff_row(self, row):
        """
        generates a alldiff constraint for a given row.

        :param row: row to create the alldiff for.
        """
        if row > 0 and row <= self.sudoku_size:
            for v in range(self.sudoku_size):  # for each value
                curr_vars = [int(str(row) + str(col+1) + str(v+1)) for col in range(self.sudoku_size)]
                # at least once
                self.rules_cnf.append(curr_vars)

                # at most once
                pairs = list(itertools.combinations(curr_vars, 2))
                pairs = [[-a, -b] for a, b in pairs]
                self.rules_cnf.extend(pairs)
        else:
            raise Exception("Row out of range!")

    def add_alldiff_row_cum(self, row):
        """
        Generates alldiff row constraint from row 1 until row 'row'
        :param row: Row up to which the constraints should be generated.
        """
        for i in range(row):
            self.add_alldiff_row(i+1)

    def add_alldiff_col(self, col):
        """
        generates a alldiff constraint for a given column.

        :param col: column to create the alldiff for.
        """
        if col > 0 and col <= self.sudoku_size:
            for v in range(self.sudoku_size):  # for each value
                curr_vars = [int(str(row + 1) + str(col) + str(v + 1)) for row in range(self.sudoku_size)]
                # at least once
                self.rules_cnf.append(curr_vars)

                # at most once
                pairs = list(itertools.combinations(curr_vars, 2))
                pairs = [[-a, -b] for a, b in pairs]
                self.rules_cnf.extend(pairs)
        else:
            raise Exception("Column out of range!")

    def add_alldiff_col_cum(self, col):
        """
        Generates alldiff col constraint from row 1 until column 'col'
        :param row: Column up to which the constraints should be generated.
        """
        for i in range(col):
            self.add_alldiff_col(i+1)

    def add_alldiff_block(self, block):
        """
        generates a alldiff constraint for a given block. Blocks are indexed starting
        from the upper left going to lower right

        :param block: block to create the alldiff for.
        """
        # get right block indices. (This is a bit messy, sorry)
        block_dim = int(sqrt(self.sudoku_size))
        block_row = int((block-1)/block_dim) + 1
        block_col = (block-1) % block_dim + 1


        # get the right indices for that block
        row_indices = []
        col_indices = []
        indices = []
        row_indices.extend([(block_row - 1) * block_dim + c + 1 for c in range(block_dim)])
        col_indices.extend([(block_col - 1) * block_dim + c + 1 for c in range(block_dim)])
        for m in range(block_dim):
            indices.extend([[row_indices[m], col_indices[c]] for c in range(block_dim)])

        # add the formulas
        for v in range(self.sudoku_size):  # for each value
            curr_vars = [int(str(i) + str(j) + str(v+1)) for i, j in indices]
            # at least one in the block must have value v
            self.rules_cnf.append(curr_vars)

            # at most one
            pairs = list(itertools.combinations(curr_vars, 2))
            pairs = [[-a, -b] for a, b in pairs]
            self.rules_cnf.extend(pairs)

    def add_alldiff_block_cum(self, block):
        """
        Generates alldiff block constraint from block 1 until block 'block'. Blocks are
        counted from left-uppermost to right-lowermost.
        :param row: block up to which the constraints should be generated.
        """
        for i in range(block):
            self.add_alldiff_block(i+1)

    def save_as_dimacs(self, filename):
        dimacs = ""

        # first line with parameters
        # this will only work for 4*4 and 9*9 sudokus
        n_vars = str(self.sudoku_size)*3
        clauses = str(len(self.rules_cnf))
        dimacs += "p cnf " + n_vars + " " + clauses + "\n"

        # write the clauses
        for c in self.rules_cnf:
            dimacs += str(c).replace(",", "")[1:-1] + " 0\n"

        with open(filename, 'w+') as f:
            f.write(dimacs)
