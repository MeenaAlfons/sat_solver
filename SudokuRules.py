import itertools


class SudokuRules:
    """
    Class to help generate the right constraints for our experiments.
    """
    def __init__(self, sudoku_size):
        """
        :param sudoku_size: size of the square sudoku. E.g. size of a 9*9 sudoku is 9.
        """
        self.sudoku_size = sudoku_size
        self.rules_cnf = []

    def add_standard_constraint(self):
        """
        Creates the constraint which states that each field must have exactly one assignment.
        :return: cnf. list of lists
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
        :return: alldiff row constraint in cnf. list of lists
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
        :return: alldiff column constraint in cnf. list of lists
        """
        pass

    def add_alldiff_block(self, block):
        """
        generates a alldiff constraint for a given block. Blocks are indexed starting
        from the upper left going to lower right

        :param block: block to create the alldiff for.
        :return: alldiff block constraint in cnf. list of lists
        """
        pass

    def save_as_dimacs(self, filename):
        dimacs = ""

        # first line with parameters
        n_vars = str(self.sudoku_size)*3
        clauses = str(len(self.rules_cnf))
        dimacs += "p cnf " + n_vars + " " + clauses + "\n"

        # write the clauses
        for c in self.rules_cnf:
            dimacs += str(c).replace(",", "")[1:-1] + " 0\n"

        print(dimacs)
        # Todo: maybe do this a bit safer to avoid overwriting?
        with open(filename, 'w+') as f:
            f.write(dimacs)
