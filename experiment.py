from dimacs_tools import load_sudoku, load_dimacs

def main():
    # load sudoku rules fo experimental constraints
    # list of strings containing the rule-filenames.
    rule_files = ['rules/sudoku-rules_4x4.txt', 'rules/sudoku-rules_9x9.txt']
    ruleset_cnfs = [load_dimacs(f) for f in rule_files]

    # load sudokus we want to test on. Modyfy 'i' to change the choosen sudokus.
    sudoku_cnfs = [load_sudoku('sudokus/1000_sudokus_9x9.txt', i) for i in range(10)]

    # for every constraint set run solver on sudoku.
    #    for each sudoku report the number of splits or other metrics and which constraint set was used

    # save results in '[expnr]_experiment.txt'
    print('whatever')
if __name__ == "__main__":
    main()