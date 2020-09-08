from SudokuRules import SudokuRules

rules = SudokuRules(4)
rules.add_standard_constraint()

rules.save_as_dimacs('test_rules.txt')