# Solution 5
from itertools import product

#I is the truth table(array) for the literals

# L is a number representing a literal, negative numbers are the negated version, zero can't be used
def evalLiteral(I,L):
    return I[abs(L)-1] if L > 0 else not I[abs(L)-1]

# C represents a clause as an array
def evalClause(I,C):
    satisfied = False
    for literal in C:
        satisfied = evalLiteral(I, literal) or satisfied
        if satisfied:
            break
    return satisfied

# A is the CNF as a 2D array
def evalCNF(A):
    isValid = True;
    isSatisfiable = False;
    
    literalSet = set()
    for clause in A:
        for literal in clause:
            literalSet.add(abs(literal))
    literalTable = list(product([True, False], repeat=len(literalSet)))

    for I in literalTable:
        clauseEval = True
        for clause in A:
            clauseEval = evalClause(I, clause) and clauseEval

        isValid = clauseEval and isValid
        isSatisfiable = clauseEval or isSatisfiable
    
    if isValid:
        print("Valid")
    elif isSatisfiable:
        print("Satisfiable")
    else:
        print("Unsatisfiable")