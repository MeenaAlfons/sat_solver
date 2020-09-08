# SatSolver

## Activate

```sh
virtualenv venv -p python3
pip3 install -r requirements.txt
source venv/bin/activate
```

## Rule files
We will test various versions of the constraints. This versions
will differ in the amount of rows/columns/boxes which are involved.
For every version a new row/column/box constraint is added to
the previous one. This makes a total of T rule sets for each
constraint type. T being the number of rows of the sudoku.

The DIMACS files follow the following structure: 
rules/[TYPE]_[NUMBER ROWS/COLS/BOXES INVOLVED]_[SUDOKU SIZE].txt
