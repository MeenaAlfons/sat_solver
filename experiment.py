from dimacs_tools import load_sudokus, load_dimacs
from InMemoryMetrics import InMemoryMetrics
from BasicDPLL import BasicDPLL
from pandas import DataFrame

def main():
    # load sudoku rules fo experimental constraints
    # list of strings containing the rule-filenames.
    rule_files = ['rules/sudoku-rules_4x4.txt', 'rules/sudoku-rules_9x9.txt']
    # for testing: ruleset_cnfs = [[[1, 2], [-1, 3], [1]],  [[1], [2]]]

    # load sudokus from file
    sudoku_cnfs = load_sudokus('sudokus/1000_sudokus_9x9.txt')

    # create dataframe for storing results.
    # Todo: we still need to decide on what our final metrics should be.
    # So deduce_count is just an example. Also other info like sudoku index might
    # be interesting.
    results = DataFrame(columns=['constraints', 'deduce_count'])

    # choose metrics
    metrics = InMemoryMetrics()
    # for every constraint set, run the solver on the test-sudokus.
    for f in rule_files:
        # load current constraint set
        rule, num_vars = load_dimacs(f)
        for sudoku in sudoku_cnfs:
            # solve if possible
            cnf = rule + sudoku
            solver = BasicDPLL(cnf, num_vars, metrics)
            result = solver.solve()[0]
            if result == 'SAT':  # We can still decide if we also want to report the UNSAT cases
                results = results.append({'constraints': f[6:-4],  # to keep just the file name
                                          'deduce_count': metrics.getDeduceCount()},
                                         ignore_index=True)
            metrics.reset()

    # save results in '[expnr]_experiment.txt'
    experiment_number = '00'
    results.to_csv(experiment_number + '_experiment.txt')


if __name__ == "__main__":
    main()