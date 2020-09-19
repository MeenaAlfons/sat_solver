#!/usr/bin/env python
"""Provides SolverComparisonExperiment
"""

import time
import argparse

from ExperimentRunner import SolverComparisonExperimentRunner

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--start',
                        metavar='start',
                        type=int,
                        help='start',
                        default=0)
    parser.add_argument('--end',
                        metavar='end',
                        type=int,
                        help='end',
                        default=1011)
    args = parser.parse_args()
    start = args.start
    end = args.end
    print("start={}, end={}".format(start, end))

    before = time.time()
    experimentRunner = SolverComparisonExperimentRunner()
    experimentRunner.run(start,end)
    print("time={} seconds".format(time.time()-before))


