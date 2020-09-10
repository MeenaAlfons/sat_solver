#!/usr/bin/env python
"""Provides validation functions
"""

import math

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

def validateCnfModel(cnf, model):
    someDontCare = False

    for clause in cnf:
        clauseIsSat = False
        for literal in clause:
            variable = abs(literal)
            if variable in model:
                value = model[variable]
                literalValue = value if literal > 0 else not value
                if literalValue == True:
                    clauseIsSat = True
                    break
            else:
                someDontCare = True

        if clauseIsSat == False:
            return False, someDontCare

    return True, someDontCare

def validateSudoku(sudokuModel, size):
    sudoku = [[0 for x in range(size)] for y in range(size)]

    for key in sudokuModel:
        if sudokuModel[key]:
            val = key%10
            key = int(key/10)
            col = key%10
            key = int(key/10)
            row = key % 10

            rowIdx = row - 1
            colIdx = col - 1

            if sudoku[rowIdx][colIdx] != 0 :
                return "Duplicate Values"
            if val < 1 or val > 9:
                return "Wrong Value"
            sudoku[rowIdx][colIdx] = val

    for row in range(size):
        bitVector = 0
        for col in range(size):
            valMask = 1 << sudoku[row][col]
            if valMask & bitVector:
                return "Value exists twice"
            bitVector |= valMask
        if bitVector != 0b1111111110:
            return "Something is wrong"

    for col in range(size):
        bitVector = 0
        for col in range(size):
            valMask = 1 << sudoku[row][col]
            if valMask & bitVector:
                return "Value exists twice"
            bitVector |= valMask
        if bitVector != 0b1111111110:
            return "Something is wrong"

    boxSize = int(math.sqrt(size))
    for box in range(size):
        bitVector = 0
        for element in range(size):
            rowIdx = int(box/boxSize) * boxSize + int(element/boxSize)
            colIdx = (box % boxSize) * boxSize + element % boxSize
            valMask = 1 << sudoku[rowIdx][colIdx]
            if valMask & bitVector:
                return "Value exists twice"
            bitVector |= valMask
        if bitVector != 0b1111111110:
            return "Something is wrong"

    return True