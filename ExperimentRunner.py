#!/usr/bin/env python
"""Provides ExperimentRunner
"""

import time
import csv
import argparse
import multiprocessing as mp

from BasicDPLL import BasicDPLL
from DummyBranchDecision import DummyBranchDecision
from RandomFalseBranchDecision import RandomFalseBranchDecision

from dimacs_tools import load_sudokus
from tools import save_csv

from Experiment import processOneSudoku, dataHeader

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

class ExperimentRunner:
    def run(self, experimentName, rulesDict, timeout, start = 0, end = 1011):
        sudokus = load_sudokus('sudokus/1000_sudokus_9x9.txt')[start:end]
        data = []

        inputValues = []
        for i in range(len(sudokus)):
            sudoku = sudokus[i]
            sudokuID = start + i + 1
            inputValues.append((sudokuID, sudoku, rulesDict, timeout))

        print("cpu_count={}".format(mp.cpu_count()))
        pool = mp.Pool(mp.cpu_count())
        results = pool.starmap(processOneSudoku, inputValues)
        pool.close()
        for result in results:
            data.extend(result)

        # Save output to csv
        filename="{}_{}_{}.csv".format(experimentName, start, end)
        save_csv(filename, dataHeader, data)
        print("")