

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

def validateSudoku(sudokuModel):
    pass