def literal2String(L):
    if(type(L)==int):
        return ('-' if (L<0) else '') + chr(ord('A')+abs(L)-1)
    elif(L[0]=='not'):
        return 'not('+term2String(L[1])+')'
    else:
        return term2String(L)

def clause2String(C):
    if(len(C)==0):
        return '{}'
    return '{ '+(', '.join([literal2String(L) for L in C]))+' }'

def clause2Sequent(C):
    if(len(C)==0):
        return '<='
    RHS = [ A[1] for A in C if A[0]=='not']
    LHS = [ A for A in C if A[0]!='not']
    if(len(RHS)==0 and len(LHS)==1):
        return term2String(LHS[0]) 
    return (', '.join([literal2String(L) for L in LHS])) + ' <= ' + (', '.join([literal2String(L) for L in RHS]))

def clauseSet2String(A):
    return '{ '+(', '.join([clause2String(C) for C in A]))+' }'

def clauseList2String(A):
    return '[ '+(', '.join([clause2String(C) for C in A]))+' ]'

def term2String(t):
    if(len(t) == 1):
        return t[0]
    else:
        return t[0] + '(' + (','.join([term2String(s) for s in t[1:]]))+')'

def substitution2String(s):
    return '{ '+(', '.join([x + ' : ' + term2String(t) for (x,t) in s.items()]))+' }'

def pprint(X1,X2=None):
    pprintAux(X1)
    if(X2!=None):
        print('\t',end='')
        pprintAux(X2)
    print()    
    
def pprintAux(X):
    #print('pprintAux:',X)
    if(type(X)==int or type(X)==tuple):              # X is literal
        print(literal2String(X),end='')
    elif(type(X)==set):            # X is a clause
        print(clause2String(X),end='')
    elif(type(X)==list):           # X is a clause list
        print(clauseList2String(X),end='')
    elif(type(X)==dict):           # X is a substitution
        D = { k:term2String(X[k]) for k in X.keys() }
        print(D,end='')
    else:
        print('Error in pprintAux!')

def getTokens(s):
    lo = hi = 0
    tokens = []
    s = s.replace(' ','')     # remove blanks
    while(hi < len(s)):
        c= s[hi]
        if(c.isalnum()):
            hi += 1
        elif(lo==hi):       # found ) ( , 
            tokens += [ s[lo:(hi+1)] ]
            lo = hi = hi+1
        else:               # found string
            tokens += [ s[lo:hi] ]
            lo = hi 
    return tokens

def getTerm(t):
    return getTermAux(getTokens(t+'$'),0)[0]
            
def getTermAux(ts,k):      # get next term starting at index k, return encoding and next index after
    # must start with string
    if(ts[k][0].isalnum()):
        if(ts[k+1] == '('):
            (tlt,next) = getTermList(ts,k+2)
            return (tuple([ts[k]] + tlt),next)
        else:       #elif(ts[k+1] == ')'):
            return ((ts[k],),k+1)
    else:
        return "Error2"

def getTermList(ts,k):  # get next term list starting at index k, return encoding and next index after
    TL = []
    while(True):
        (t,k) = getTermAux(ts,k)
        TL.append(t)
        if(ts[k]==')'):
            return (TL,k+1)
        elif(ts[k]==','):
            k += 1

def reportError(s,i,follow):
    print('Parsing error: expecting\n')
    print('\t',end='')
    for c in follow:
        print(c+'  ',end='')
    print('\n\nhere:\n')
    print('\t'+s[:-1]+'\n\t'+(' '*i)+'^')    

def parse(s,trace=False):
    s += '$'
    stack = [1]
    i=0
    while(True):
        if trace:
            print(s[i],stack)
        state = stack[-1]      # top state on stack
        if(state == 0):
            if(s[i] == '$'):
                return stack[1]
            else:
                reportError(s,i,['<end of expression>'])
                return
        elif(state in [1,3,5]):
            if(s[i].isalnum()):
                stack += [s[i],6]
                i += 1
            else:
                reportError(s,i,['<letter or number>'])
                return
        elif(state == 2):
            if(s[i] == '('):
                stack += [s[i],3]
                i += 1
            elif(s[i] in '),$'):    # reduce by 1: E -> S
                exp = stack[-2]
                stack.pop()
                stack.pop()
                if(stack[-1]==1):
                    stack += [(exp,),0]
                elif(stack[-1] in [3,5]):
                    stack += [(exp,),4]
            else:
                reportError(s,i,['(',')','<letter or number>','<end of expression>'])
                return
        elif(state == 4):
            if(s[i] == ','):
                stack += [s[i],5]
                i += 1
            elif(s[i] == ')'):      # reduce by 5: EL -> E
                exp = stack[-2]
                stack.pop()
                stack.pop()
                if(stack[-1]==3):
                    stack += [[exp],9]
                elif(stack[-1]==5):
                    stack += [[exp],8]
            else:
                reportError(s,i,[',',')'])
                return
        elif(state == 6):
            if(s[i].isalnum()):
                stack += [s[i],6]
                i += 1
            elif(s[i] in '(),$'):    # reduce by 3: S -> let
                let = stack[-2]
                stack.pop()
                stack.pop()
                if(stack[-1] in [1,3,5]):
                    stack += [let,2]
                elif(stack[-1] == 6):
                    stack += [let,7]
            else:
                reportError(s,i,['(',')','<letter or number>','<end of expression>'])
                return
        elif(state == 7):
            if(s[i] in '(),$'):    # reduce by 4: S -> let S
                exp = stack[-4]+stack[-2]
                stack.pop()
                stack.pop()
                stack.pop()
                stack.pop()
                if(stack[-1] in [1,3,5]):
                    stack += [exp,2]
                elif(stack[-1] == 6):
                    stack += [exp,7]
            else:
                reportError(s,i,['(',',',')','<end of expression>'])         
                return
        elif(state == 8):
            if(s[i] in ')'):    # reduce by 6: EL -> E,EL
                exp = [stack[-6]] + stack[-2]
                stack.pop()
                stack.pop()
                stack.pop()
                stack.pop()
                stack.pop()
                stack.pop()
                if(stack[-1]==3):
                    stack += [exp,9]
                elif(stack[-1]==5):
                    stack += [exp,8]
            else:
                reportError(s,i,[')'])
                return
        elif(state == 9):
            if(s[i]==')'):
                stack += [s[i],10]
                i += 1
            else:
                reportError(s,i,[')'])
                return
        elif(state == 10):
            if(s[i] in '),$'):        # reduce by 2: E -> S(EL)
                exp = tuple([stack[-8]] + stack[-4])
                stack.pop(); stack.pop()
                stack.pop(); stack.pop()
                stack.pop(); stack.pop()
                stack.pop(); stack.pop()
                if(stack[-1]==1):
                    stack += [exp,0]
                elif(stack[-1] in [3,5]):
                    stack += [exp,4]     
            else:
                reportError(s,i,[')',',','<end of expression>'])          
                return
            
def parseClause(S):      # S is a list of strings representing atomic formulae
    return { parse(t) for t in S }

def parseClauseList(L):
    return [ parseClause(C) for C in L ]

def isVar(t):
    return len(t)==1 and t[0][0] in ['u','v','w','x','y','z']    # any string starting with u,v,w,x, y, z

def isConst(t):
    return len(t)==1 and not (t[0][0] in ['u','v','w','x','y','z'])

def getVars(t,vs=set()):
    if(type(t)==set):
        for k in t:
            vs = vs.union(getVars(k,vs))
        return vs 
    elif(isVar(t)):
        return {t[0]}
    elif(isConst(t)):
        return set()
    else:
        for k in range(1,len(t)):
            vs = vs.union(getVars(t[k],vs))
        return vs        

def occursIn(v,t):
    if(isVar(t)):
        return ((v,) == t)
    elif(isConst(t)):
        return False
    else:
        return any( [ occursIn(v,s) for s in t[1:] ] )
    
def applySubst(t,subst):
    if(type(t)==set):
        return { applySubst(c,subst) for c in t}   
    elif(isVar(t) and t[0] in subst.keys()):
        return subst[t[0]] 
    elif(isConst(t)):
        return t
    else:
        return tuple([t[0]] + [ applySubst(t[k],subst) for k in range(1,len(t)) ] )
            
def composeSubst(sub1,sub2):
    s = { v : applySubst(t,sub2) for (v,t) in sub1.items() }
    s.update(sub2)
    return s

def unify(s,t,subst={}):
    s = applySubst(s,subst)
    t = applySubst(t,subst)
    if(s==t):
        return subst
    if(isVar(t)):
        (s,t) = (t,s)
    if(isVar(s)):
        if(occursIn(s[0],t)):
            return None
        else:
            return composeSubst(subst,{s[0]:t})
    if(s[0] != t[0] or len(s)!=len(t)):
        return None
    for k in range(1,len(s)):
        subst = unify(s[k],t[k],subst)
        if(subst==None):
            return None
    return subst

seed = 0

def reseed():
    global seed
    seed = 0
    
def getNewVariable():
    global seed
    seed += 1
    return ('x' + str(seed-1),)

def rename(t):
    rs = { v : getNewVariable() for v in getVars(t)}
    return applySubst(t,rs)

def resolveFOL(C1,C2):
    C1 = rename(C1)
    C2 = rename(C2)
    R = []
    for L1 in C1:
        for L2 in C2:
            if(L1[0]=='not' and L2!='not'):  # complementary literals
                usub = unify(L1[1],L2)
                if(usub != None):
                    T1 = set(C1)
                    T1.remove(L1)
                    T2 = set(C2)
                    T2.remove(L2)
                    R.append( applySubst(T1.union(T2),usub) )
            elif(L2[0]=='not' and L1!='not'):  # complementary literals
                usub = unify(L2[1],L1)
                if(usub != None):
                    T2 = set(C2)
                    T2.remove(L2)
                    T1 = set(C1)
                    T1.remove(L1)
                    R.append( applySubst(T1.union(T2),usub) )
    return R
                
def resolveAllFOL(A,C):
    R = [ resolveFOL(C1,C) for C1 in A ]
    return [C for CL in R for C in CL]

def proveFOL(KB,SOS,limit=30,trace=False):
    Queue = SOS
    count = 0                   # count the number of pops off the queue
    while(len(Queue) > 0):
        if(trace):
            print('Queue:', clauseList2String(Queue))
        # form all resolvents with front of queue, 
        # check if empty clause is generated, else add to end of queue
        C = Queue.pop()
        count += 1
        for C1 in resolveAllFOL(KB + Queue,C):
            if(len(C1) == 0):
                print("\nUnsatisfiable! (",count,"step(s) executed )")
                return
            else:   
                Queue = [C1] + Queue        # BFS 
                Queue.sort(reverse=True, key=(lambda x: len(x)))
        if(count >= limit):
            print("\nEmpty clause not found after", limit,"steps!")
            return
    print("\nSatisfiable! (",count,"step(s) executed )")


# problems 

KB1b= [
    {'Female(KarenA)'}, {'Male(FranzA)'}, {'Female(AnneA)'}, {'Male(OscarA)'}, {'Female(MaryB)'}, {'Male(OscarB)'},
    {'Male(HenryA)'}, {'Female(EveA)'}, {'Female(IsabelleA)'}, {'Male(ClydeB)'}, 
    {'Child(OscarA,KarenA,FranzA)'}, {'Child(MaryB,KarenA,FranzA)'}, {'Child(HenryA,AnneA,OscarA)'},
    {'Child(EveA,AnneA,OscarA)'}, {'Child(IsabellaA,AnneA,OscarA)'}, {'Child(ClydeB,MaryB,OscarB)'},
    { 'Son(x,y)', 'not(Child(x,z,y))', 'not(Male(x))' }, { 'Son(x,y)', 'not(Child(x,y,z))', 'not(Male(x))' },
    { 'Daughter(x,y)', 'not(Child(x,y,z))', 'not(Female(x))' }, { 'Daughter(x,y)', 'not(Child(x,z,y))', 'not(Female(x))' },
    { 'Father(x,y)', 'not(Child(y,z,x))', 'not(Male(x))' },
    { 'Mother(x,y)', 'not(Child(y,x,z))', 'not(Female(x))' },
    { 'Parent(x,y)', 'not(Child(y,x,z))' }, { 'Parent(x,y)', 'not(Child(y,z,x))' },
    { 'Grandfather(x,y)', 'not(Male(x))', 'not(Child(y,v,w))', 'not(Child(v,z,x))'},
    { 'Grandfather(x,y)', 'not(Male(x))', 'not(Child(y,v,w))', 'not(Child(w,z,x))'},
    { 'Grandmother(x,y)', 'not(Female(x))', 'not(Child(y,v,w))', 'not(Child(v,x,z))'},
    { 'Grandmother(x,y)', 'not(Female(x))', 'not(Child(y,v,w))', 'not(Child(w,x,z))'},
    
    # new clauses
    {'Brother(x,y)', 'not(Child(x,z,w))', 'not(Child(y,z,w))','not(Male(x))' },
    {'Sister(x,y)', 'not(Child(x,z,w))', 'not(Child(y,z,w))','not(Female(x))' }
]

KB1b = parseClauseList(KB1b)

# clyde has a brother - should be satisfiable
SOS1 = parseClauseList([ { 'not(Brother(x,ClydeB))' } ])
proveFOL(KB1b,SOS1,trace=True)