from math import sqrt

def load_dimacs(filename):
    with open(filename) as f:
        rules = f.read()
        # split between clauses and drop las (empty) clause
        rules = rules.replace('\n', '').split(' 0')[:-1]

        # split clauses and cast to int
        rules = [[int(l) for l in c.split(' ')] for c in rules][:-1]

        return rules

def load_sudoku(filename, which):
    """
    Loads a sudoku form a collection and returns the DIMACS format of it.
    Works only for square sudokus.

    :param filename: File with the sudoku collection.
    :param which: The index of the sudoku that is choosen from the collection.
    :return: DIMACS clauses representing the sudoku instance.
    """
    with open(filename) as f:
        # read all sudokus
        sudokus = f.readlines()
        # choose one and trim 'newline'
        sudoku = sudokus[which][:-1]
        size = int(sqrt(len(sudoku)))

        sudoku_instance_cnf = []
        position = 0  # counter for position in the string
        for row in range(size):
            for col in range(size):
                if sudoku[position] != '.':
                    sudoku_instance_cnf.append([int(str(row+1) + str(col+1) + sudoku[position])])
                position += 1

        return sudoku_instance_cnf