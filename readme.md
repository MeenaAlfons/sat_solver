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

## Experiment 2

The basic command for experiment 2 looks like this:

```sh
python3 DiffConstraintsExperiment.py [--start start] [--end end] numOfContraints
```

which means there is a required argument called `numOfContraints` and optional
flags `--start` and `--end` which help in splitting the dataset into multiple executions.

Each execution will result in a file named according to this template:
```
constraints_<numOfContraints>_<start>_<end>.csv
```
This guarantees that all successfull executions will be writted to different files.

Example:
```sh
# This means 13 contraints and will run all sudokus starting from 0 and ending before 1011
# Note that we have 1011 sudokus in the file
python3 DiffConstraintsExperiment.py 13 --start 0 --end 1011

# this will result in a file called constraints_13_0_1011.csv
```
Another example
```sh
# This means 0 contraints and will run all sudokus starting from 0 and ending before 500
python3 DiffConstraintsExperiment.py 0 --start 0 --end 500

# this will result in a file called constraints_0_0_500.csv
```
Whether you run those experiments on your machine or in Google Colab you could use the following script:
```sh
git clone git@github.com:sa-and/sat_solver.git
cd sat_solver
python3 DiffConstraintsExperiment.py 13 --start 0 --end 1011
```
And change the numOfConstraints, start and end as you see fit.

Remember to copy the output file to a safe place and send it to us.
