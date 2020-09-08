class ConstraintGenerator:
    """
    Class to help generate the right constraints for our experiments.
    """
    def __init__(self, sudoku_size):
        """
        :param sudoku_size: size of the square sudoku. E.g. size of a 9*9 sudoku is 9.
        """
        self.sudoku_size = sudoku_size

    def standard_constraint(self):
        """
        Creates the constraint which states that each field must have exactly one assignment.
        :return: cnf. list of lists
        """

    def alldiff_row(self, row):
        """
        generates a alldiff constraint for a given row.

        :param row: row to create the alldiff for.
        :return: alldiff row constraint in cnf. list of lists
        """
        pass

    def alldiff_col(self, col):
        """
        generates a alldiff constraint for a given column.

        :param col: column to create the alldiff for.
        :return: alldiff column constraint in cnf. list of lists
        """
        pass

    def alldiff_block(self, block):
        """
        generates a alldiff constraint for a given block. Blocks are indexed starting
        from the upper left going to lower right

        :param block: block to create the alldiff for.
        :return: alldiff block constraint in cnf. list of lists
        """
        pass
