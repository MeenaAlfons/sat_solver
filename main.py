#!/usr/bin/env python
"""Provides main function for testing SatSolvers
"""

from SatInterface import SatInterface
from BasicDPLL import BasicDPLL

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

def main():
    print("Hello World!")
    cnf = [[1,2,3], [1,-2],[1,-3],[-1,3]]
    numOfVars = 3

    solvers = [ SatInterface(cnf,numOfVars), BasicDPLL(cnf,numOfVars) ]

    for solver in solvers:
        result, model = solver.solve()
        print("result={}, model={}".format(result, model))

if __name__ == "__main__":
    main()