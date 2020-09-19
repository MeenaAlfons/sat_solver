#!/usr/bin/env python
"""Provides ConstraintRulesGenerator
"""

from SudokuRules import SudokuRules

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

class ConstraintRulesGenerator():
    def __init__(self):
        self.rulesCreator = SudokuRules(9)

    def cumulativeRulesOf(self, rows, cols, blocks):
        name = "r{}_c{}_b{}".format(rows, cols, blocks)

        self.rulesCreator.reset()
        if rows > 0:
            self.rulesCreator.add_alldiff_row_cum(rows)

        if cols > 0:
            self.rulesCreator.add_alldiff_col_cum(cols)

        if blocks > 0:
            self.rulesCreator.add_alldiff_block_cum(blocks)

        return name, self.rulesCreator.getRules()


    def allCummulativeCombinations(self, numOfConstraints):
        rulesDict = {}
        # the following nested loop go throw all the combinations of rows, cols, blocks
        # Where each one of them could have values from 0 to 9
        # However the script only considers combinations which add up to the numOfConstraints
        # Example combinations when numOfConstraints=7:
        # row=0 col=0 blocks=7
        # row=1 col=3 blocks=3
        # row=6 col=0 blocks=1
        for row in range(9+1):
            if row == numOfConstraints:
                name, rules = self.cumulativeRulesOf(row, 0, 0)
                rulesDict[name] = (rules, numOfConstraints)
                break
            for col in range(9+1):
                if row + col == numOfConstraints:
                    name, rules = self.cumulativeRulesOf(row, col, 0)
                    rulesDict[name] = (rules, numOfConstraints)
                    break
                for block in range(9+1):
                    if row + col + block == numOfConstraints:
                        name, rules = self.cumulativeRulesOf(row, col, block)
                        rulesDict[name] = (rules, numOfConstraints)
                        break

        return rulesDict

    def singleCummulative(self, numOfConstraints):
        rows = 0
        cols = 0
        blocks = 0

        if numOfConstraints <=9:
            rows = numOfConstraints
        elif numOfConstraints <= 18:
            rows = 9
            cols = numOfConstraints - 9
        elif numOfConstraints <= 27:
            rows = 9
            cols = 9
            blocks = numOfConstraints - 18
        else:
            raise "Not implemented"

        name, rules = self.cumulativeRulesOf(rows, cols, blocks)
        return name, rules

    def singleCummulativeForEachConstraint(self):
        rulesDict = {}
        for numOfConstraints in range(0,27+1):
            name, rules = self.singleCummulative(numOfConstraints)
            rulesDict[name] = (rules, numOfConstraints)
        return rulesDict