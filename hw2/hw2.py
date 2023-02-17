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

def literal2String(L):
    return ('-' if (L<0) else '') + chr(ord('A')+abs(L)-1)

def clause2String(C):
    if(C=={}):
        return '{}'
    else:
        return '{ '+(', '.join([literal2String(L) for L in C]))+' }'

def clauseList2String(A):
    return '[ '+(', '.join([clause2String(C) for C in A]))+' ]'

def pprint(X):
    if(type(X)==int):              # X is literal
        print(literal2String(X))
    elif(type(X)==set):            # X is a clause
        print(clause2String(X))
    elif(type(X)==list):           # X is a clause list
        print(clauseList2String(X))
    else:
        print('Error in pprint!')

## PROBLEM 1

def resolve(C1,C2):
    resolvents = []
    for literal1 in C1:
        for literal2 in C2:
            if literal1 == -literal2:
                resolvent = (C1 - {literal1}) | (C2 - {literal2})
                if resolvent not in resolvents:
                    resolvents.append(resolvent)
    return resolvents

def resolveAll(A,C):   
    resolvents = []
    for clause in A:
        new_resolvents = resolve(clause, C)
        resolvents.extend(new_resolvents)
    return resolvents

def prove1(CL, limit=30, trace=True):
    queue = CL
    visited = set()
    steps = 0
    while queue and steps < limit:
        steps += 1
        current = queue.pop(0)
        if trace:
            print(f"Step {steps}: {current}")
        for resolvent in resolveAll(queue, current):
            if len(resolvent) == 0:
                print(f"Unsatisfiable. Number of steps: {steps}")
                return
            elif frozenset(resolvent) not in visited:
                queue.append(resolvent)
                visited.update(frozenset(resolvent))
    if steps == limit:
        print(f"Not proven after {limit} steps.")
    else:
        print(f"Satisfiable. Number of steps: {steps}")

# tests: first 3 are unsatisfiable, test 4 is satisfiable

# print('\ntest a','\n------')
# CL1a = [ {2}, {-2} ]     

# print('CL1a: ',end=''); pprint(CL1a); print()
# prove1(CL1a); print()

# print('test b','\n------')
# CL1b = [ {1}, {-1,2}, {-2,3}, {-3,4}, {-4} ]

# print('CL1b: ',end=''); pprint(CL1b); print()
# prove1(CL1b); print()

# print('test c','\n------')
# CL1c = [ {1}, {-1,2,3}, {-3,4}, {-3,5}, {-5}, {-2} ]

# print('CL1c: ',end=''); pprint(CL1c); print()
# prove1(CL1c); print()

# print('test d','\n------')
# CL1d = [ {1}, {-1,2,3}, {-3,4}, {-3,5}, {-5} ]

# print('CL1d: ',end=''); pprint(CL1d); print()
# prove1(CL1d); print()

# CL2a = [{1, -2}, {2, -1}, {-1, -2}]
# print('CL2a:',end=''); pprint(CL2a); print()
# prove1(CL2a, 100, True); print()
# evalCNF(CL2a)

# CL2b = [{-1, -2}, {-1, 2}, {1, -2}, {1, 2}]
# print('CL2b: ',end=''); pprint(CL2b); print()
# prove1(CL2b, 30, True); print()
# evalCNF(CL2b)

# CL2d = [{-1, -2, -3}, {-1, -2, 3}, {-1, 2, -3}, {-1, 2, 3}, {1, -2, -3}, {1, -2, 3}, {1, 2, -3}, {1, 2, 3}]
# print('CL2d: ',end=''); pprint(CL2d); print()
# evalCNF(CL2d); print()
# # prove1(CL2d, 3, True); print()
# # prove1(CL2d, 4, True); print()
# # prove1(CL2d, 5, True); print()

# prove1(CL2d, 15, False); print()

def prove3(KB, SOS, limit=30, trace=True):
    queue = SOS
    visited = set()
    steps = 0
    while queue and steps < limit:
        steps += 1
        current = queue.pop(0)
        if trace:
            print(f"Step {steps}: {current}")
        
        if not current:
            print(f"Unsatisfiable. Number of steps: {steps}")
            return
        
        for resolvent in resolveAll(KB + queue, current):
            if len(resolvent) == 0:
                print(f"Unsatisfiable. Number of steps: {steps}")
                return
            elif frozenset(resolvent) not in visited:
                queue.append(resolvent)
                visited.update(frozenset(resolvent))

    if steps == limit:
        print(f"Not proven after {limit} steps.")
    else:
        print(f"Satisfiable. Number of steps: {steps}")

# print('\ntest a','\n------')
# KB3a1 = [ {2} ]
# SOS3a1 = [ {-2} ]

# print('KB3a1: ',end=''); pprint(KB3a1); 
# print('SOS3a1: ',end=''); pprint(SOS3a1); print()
# prove3(KB3a1,SOS3a1); print()

# print('test b','\n------')
# KB3a2 = [ {1}, {-1,2}, {-2,3}, {-3,4} ]
# SOS3a2 = [ {-4} ]

# print('KB3a2: ',end=''); pprint(KB3a2);
# print('SOS3a2: ',end=''); pprint(SOS3a2); print()
# prove3(KB3a2,SOS3a2); print()

# print('test c','\n------')
# KB3a3 = [ {1}, {-1,2,3}, {-3,4}, {-3,5}, {-5} ]
# SOS3a3 = [ {-2} ]

# print('KB3a3: ',end=''); pprint(KB3a3);
# print('SOS3a3: ',end=''); pprint(SOS3a3); print()
# prove3(KB3a3,SOS3a3); print()

# print('test d','\n------')
# KB3a4 = [ {1}, {-1,2,3}, {-3,4}, {-3,5} ]
# SOS3a4 = [ {-5} ]

# print('KB3a4: ',end=''); pprint(KB3a4);
# print('SOS3a4: ',end=''); pprint(SOS3a4); print()
# prove3(KB3a4,SOS3a4); print()

KB3c1 = [{-1, -2, -3}, {-1, -2, 3}, {-1, 2, -3}, {-1, 2, 3}, {1, -2, -3}, {1, -2, 3}, {1, 2, -3}]
SOS3c1 = [{1, 2, 3}]

print('KB3c1: ',end=''); pprint(KB3c1);
print('SOS3c1: ',end=''); pprint(SOS3c1); print()

# prove3(KB3c1, SOS3c1, 3, True); print()
# prove3(KB3c1, SOS3c1, 4, True);prove3(CL2d, 4, True); print()
# prove3(KB3c1, SOS3c1, 5, True); print()

prove3(KB3c1, SOS3c1, 15, False); print()
# prove3(KB3c1, SOS3c1, 20, False); print()v

