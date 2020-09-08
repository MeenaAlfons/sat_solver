from SudokuRules import SudokuRules

rules = SudokuRules(4)
#rules.add_standard_constraint()
#rules.add_alldiff_row_cum(4)
rules.add_alldiff_col_cum(4)

rules.save_as_dimacs('test_rules.txt')