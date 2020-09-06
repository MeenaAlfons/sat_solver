#!/usr/bin/env python
"""Provides TestBasicDPLL which tests BasicDPLL
"""

import unittest
from TestSatSolver import TestSatSolver
from BasicDPLL import BasicDPLL

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

class TestBasicDPLL(TestSatSolver):
    def test(self):
        """
        Test BasicDPLL
        """
        self.setSatSolverClass(BasicDPLL)
        self.all()

if __name__ == '__main__':
    unittest.main()
