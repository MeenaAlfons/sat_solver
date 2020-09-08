from math import sqrt


def load_dimacs(filename):
    """
    Loads a cnf problem in DIMACS format and returns the clauses as list of lists and the
    number of variables in the problem.

    :param filename: File containing the SAT problem in DIMACS format
    :return: tuple of clauses and number of variables (none if not provided)
    """
    cnf = ""
    with open(filename) as f:
        for line in f.readlines():
            # read the parameters
            if line[0] == 'p':
                n_vars = line.split(' ')[2]
            # ignore comments
            elif line[0] == 'c':
                pass
            # filter out actual clauses
            else:
                cnf += line

        # split between clauses and drop las (empty) clause
        cnf = cnf.replace('\n', '').split(' 0')[:-1]

        # split clauses and cast to int
        cnf = [[int(l) for l in c.split(' ')] for c in cnf][:-1]

        return (cnf, n_vars)

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