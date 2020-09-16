#!/usr/bin/env python
"""Provides TestSatSolver with test cases for any SatSolverInterface
"""

import unittest
from InMemoryMetrics import InMemoryMetrics
from DummyBranchDecision import DummyBranchDecision
import validation

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

class TestSatSolver(unittest.TestCase):
    def setSatSolverClass(self, SatSolverClass):
        self.SatSolverClass = SatSolverClass

    def all(self):
        """
        Test All cases for SatSolver
        """
        testCases = [{
            "cnf": [[-1],[2]],
            "numOfVars": 2,
            "expectedResult": "SAT",
            "expectDontCare": False
        },{
            "cnf": [[-1,2]],
            "numOfVars": 2,
            "expectedResult": "SAT",
            "expectDontCare": False
        },{
            "cnf": [[1,2,3], [1,-2],[1,-3],[-1,3]],
            "numOfVars": 3,
            "expectedResult": "SAT",
            "expectDontCare": False
        }]

        metrics = InMemoryMetrics()
        for test in testCases:
            solver = self.SatSolverClass(test["cnf"], test["numOfVars"], DummyBranchDecision(), -1, metrics)
            result, model = solver.solve()
            self.assertEqual(result, test["expectedResult"], test)
            if test["expectedResult"] == "SAT":
                isSat, someDontCare = validation.validateCnfModel(test["cnf"], model)
                self.assertTrue(isSat, test)
                self.assertEqual(test["expectDontCare"], someDontCare, test)
