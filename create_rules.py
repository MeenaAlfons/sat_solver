from SudokuRules import SudokuRules
"""
Script for creating the sets of rules needed for our experiment.

Three types of constraint sets will be created:
1. The standard row constraint of Sudoku.
2. The standard column constraint of Sudoku.
3. The standard box constraint of Sudoku.
Each of them also contains the basic constraint that each field
must contain exactly one number.

We will test various versions of the constraints. This versions
will differ in the amount of rows/columns/boxes which are involved.
For every version a new row/column/box constraint is added to
the previous one. This makes a total of T rule sets for each
constraint type. T being the number of rows of the sudoku.

The DIMACS files follow the following structure:
rules/[TYPE]_[NUMBER ROWS/COLS/BOXES INVOLVED]_[SUDOKU SIZE].txt
"""
size = 9
# create rule generator for 9x9 Sudoku
rules = SudokuRules(size)

for s in range(size):
    # create files for rows
    rules.reset()
    rules.add_alldiff_row_cum(s+1)
    rules.save_as_dimacs('rules/row_'+str(s+1)+"_"+str(size)+".txt")

    # create files for columns
    rules.reset()
    rules.add_alldiff_col_cum(s+1)
    rules.save_as_dimacs('rules/col_' + str(s + 1) + "_" + str(size) + ".txt")

    # create files for boxes
    rules.reset()
    rules.add_alldiff_block_cum(s+1)
    rules.save_as_dimacs('rules/box_' + str(s + 1) + "_" + str(size) + ".txt")
