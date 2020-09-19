#!/usr/bin/env python
"""Provides Experiment
"""
import time

from BasicDPLL import BasicDPLL
from InMemoryMetrics import InMemoryMetrics
from RandomFalseBranchDecision import RandomFalseBranchDecision

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

dataHeader = ["sudokuID", "name", "numOfConstraints", "result", "totalTime", "loop", "backtrack", "flip", "unit"]

def processOneSudoku(sudokuID, sudoku, rulesDict, timeout):
    decisionHeuristicFactory = RandomFalseBranchDecision
    numOfVars = 9
    data = []
    for name in rulesDict:
        rules, numOfConstraints = rulesDict[name]
        cnf = rules + sudoku
        instanceMetrics = InMemoryMetrics()

        before = time.time()
        solver = BasicDPLL(cnf,
            numOfVars,
            decisionHeuristicFactory,
            timeout,
            5,
            instanceMetrics
        )
        result, _ = solver.solve()
        totalTime = time.time()-before
        counters = instanceMetrics.getCounters()
        if result == "TIMEOUT":
            print("T", end='', flush=True)
        data.append((
            sudokuID,
            name,
            numOfConstraints,
            result,
            totalTime,
            counters.get("loop", 0),
            counters.get("backtrack", 0),
            counters.get("flip", 0),
            counters.get("unit", 0),
        ))
    print(".", end='', flush=True)
    return data

heuristicDataHeader = ["sudokuID", "name", "result", "totalTime", "loop", "backtrack", "flip", "unit"]

def processOneSudokuWithHeuristic(sudokuID, sudoku, rules, heuristicDict):
    numOfVars = 9
    data = []
    for name in heuristicDict:
        decisionHeuristicFactory = heuristicDict[name]
        cnf = rules + sudoku
        instanceMetrics = InMemoryMetrics()

        before = time.time()
        solver = BasicDPLL(cnf,
            numOfVars,
            decisionHeuristicFactory,
            -1,
            0,
            instanceMetrics
        )
        result, _ = solver.solve()
        totalTime = time.time()-before
        counters = instanceMetrics.getCounters()
        if result == "TIMEOUT":
            print("T", end='', flush=True)
        data.append((
            sudokuID,
            name,
            result,
            totalTime,
            counters.get("loop", 0),
            counters.get("backtrack", 0),
            counters.get("flip", 0),
            counters.get("unit", 0),
        ))
    print(".", end='', flush=True)
    return data
