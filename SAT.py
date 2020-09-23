import sys
import time
import argparse

from InMemoryMetrics import InMemoryMetrics
from BasicDPLL import BasicDPLL
from dimacs_tools import load_dimacs

from RandomBranchDecision import RandomBranchDecision
from RandomFalseBranchDecision import RandomFalseBranchDecision
from DummyBranchDecision import DummyBranchDecision
from DynamicLargestIndividualSum import DynamicLargestIndividualSum
from DynamicLargestCombinedSum import DynamicLargestCombinedSum
from JeroslowWangOneSided import JeroslowWangOneSided

from DeliveredSolvers import DeliveredSolvers

if __name__ == "__main__":
    args = sys.argv
    solverChoice = args[1]
    filename = args[2]
    solverNumber = int(solverChoice.replace("-S", ""))
    print("solverNumber={}, filename={}".format(solverNumber, filename))

    deliveredSolvers = DeliveredSolvers()
    deliveredSolvers.execute(solverNumber, filename)
