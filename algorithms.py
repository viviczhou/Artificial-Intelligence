'''
Project #2 Automated Reasoning
Version 2.0 created at 2019/10/23
    Algorithms implemented: TT_Entails, PL_Resolve, DPLL_Satisfiable
'''

from tools import *
import time

class KB:
    """Knowledge Base for propositional logic"""
    def __init__(self, sentence=None):
        self.clauses = []
        if sentence:
            self.tell(sentence)

    def tell(self, sentence):
        # add the sentence's clauses to the KB
        self.clauses.extend(list_clauses('&', [toCNF(sentence)]))

    def ask(self, query):
        # if entails, yield {} (empty set = false), else no result yield
        if TT_Entails(Expr('&', *self.clauses), query): #input is in CNF
            yield {}

    def model_checking(self, query):
        for _ in self.ask(query): # not no result, entails
            return True
        return False

###########################################################################################

def TT_Entails(kb, alpha):
    symbols = list(list_symbols(kb & alpha))
    return TT_Check_All(kb, alpha, symbols, {})

def TT_Check_All(kb, alpha, symbols, model):
    if not symbols: # symbols is empty
        if PL_True(kb, model): # kb is true
            result = PL_True(alpha, model)
            return result
        else: # always return true when kb is false
            return True
    else:
        P, rest = symbols[0], symbols[1:]
        T_model = model.copy()
        T_model[P] = True
        F_model = model.copy()
        F_model[P] = False
        return (TT_Check_All(kb, alpha, rest, T_model) and
                TT_Check_All(kb, alpha, rest, F_model))

def list_symbols(pl):
    # a set of the proposition symbols in KB and alpha
    if ((isinstance(pl.op, str) and pl.op[:1].isalpha()) and pl.op[0].isupper()): # is just a symbol
        return {pl}
    else:
        symbols = set()
        for arg in pl.args:
            for symbol in list_symbols(arg):
                symbols.add(symbol)
        return symbols

def PL_True(exp, model):
    # return True if the propositional logic expression is true in the model, else return false, and none if not spesified.
    if exp in (True, False):
        return exp
    op, args = exp.op, exp.args
    if ((isinstance(op, str) and op[:1].isalpha()) and op[0].isupper()): # atoms
        return model.get(exp)
    elif op == '&':
        for arg in args:
            if PL_True(arg, model) == False:
                return False
        return True
    elif op == '|':
        for arg in args:
            if PL_True(arg,model)==True:
                return True
        return False
    elif op == '~':
        arg = args[0]
        return not(PL_True(arg, model))
    elif op == '==>':
        left = args[0]
        right = args[1]
        if PL_True(left,model) == PL_True(right,model)==False:
            return False
        return True
    elif op == '<=>':
        left = args[0]
        right = args[1]
        if PL_True(left,model) == PL_True(right,model):
            return True
        return False

######################################################################################

def PL_Resolution(KB, alpha):
    clauses = KB.clauses + list_clauses('&', [toCNF(~alpha)])
    new = set()
    start_time = time.time()
    out_of_time = 'Maybe'
    while True:# loop do, prevent the program from running forever
        pairs = []
        for ci in clauses:
            for cj in clauses:
                if ci != cj:
                    pairs.append([ci,cj])
        for (ci, cj) in pairs:
            resolvents = PL_Resolve(ci, cj, start_time)
            if (time.time() - start_time) > 60:
                return out_of_time
            if False in resolvents: # {} is False, if resolvents contains {}, then return True
                return True
            new = new.union(set(resolvents))
        if new.issubset(set(clauses)):
            return False
        for c in new:
            if c not in clauses:
                clauses.append(c)

def PL_Resolve(ci, cj, start_time):
    # return all clauses that can be obtained by resolving clauses ci and cj
    clauses = []
    d_ci = list_clauses('|', [ci])
    d_cj = list_clauses('|', [cj])
    for di in d_ci: # check disjunctions pair by pair, one by one
        for dj in d_cj:
            if di == ~dj or ~di == dj:
                new_symbol = []
                new_d_ci = []
                new_d_cj = []
                for i in d_ci:
                    if i != di:
                        new_d_ci.append(i)
                for j in d_cj:
                    if j != dj:
                        new_d_cj.append(j)
                new_symbol += new_d_ci
                new_symbol += new_d_cj
                d_new = list(set(new_symbol))
                clauses.append(combine_cluases('|', d_new))
            if (time.time() - start_time) > 60:
                break
    return clauses

###############################################################################################
def DPLL_Satisfiable(s):
    # Check whtner a propositional sentence is satisfiable or not.
    # The function find_pure_symbol is passed a list of unknown clauses (not all clauses and the model, different from 7.17)
    clauses = list_clauses('&', [toCNF(s)]) # all clauses
    symbols = list(list_symbols(s))
    return DPLL(clauses, symbols, {})

def DPLL(clauses, symbols, model):
    # See if the clauses are true in a partial model.
    unknown_clauses = []  # clauses with an unknown truth value
    for c in clauses: # if every\some clause in clauses is true\false in model then return true\false.
        value = PL_True(c, model)
        if value is False: # false exists, not all true
            return False
        if value is not True: # false not exists, but value not true, value unknown
            unknown_clauses.append(c)
    if not unknown_clauses: # no unknown clause, return true
        return True
    P, value = Find_Pure_Symbol(symbols, unknown_clauses)
    if P: # not null
        new_p = []
        new_P = []
        if isinstance(symbols, str):
            symbols.replace(P, '')
        if not isinstance(symbols, str):
            for i in symbols:
                if i != P:
                    new_P.append(i)
        new_p += new_P
        new_model = model.copy()
        new_model[P] = value
        return DPLL(clauses, new_p, new_model) # symbols - P, model.union(P=value)
    P, value = Find_Unit_Clause(clauses, model)
    if P:# not null
        new_p = []
        new_P = []
        if isinstance(symbols, str):
            symbols.replace(P, '')
        if not isinstance(symbols, str):
            for i in symbols:
                if i != P:
                    new_P.append(i)
        new_p += new_P
        new_model = model.copy()
        new_model[P] = value
        return DPLL(clauses, new_p, new_model) # symbols - P, model.union(P=value)
    if not symbols: # null
        raise TypeError
    P, rest = symbols[0], symbols[1:] # first and rest
    T_model = model.copy()
    T_model[P] = True
    F_model = model.copy()
    F_model[P] = False
    return (DPLL(clauses, rest, T_model) or DPLL(clauses, rest, F_model))

def Find_Pure_Symbol(symbols, clauses):
    # Find a symbol and its value if it appears only as a positive(return true)\negative(return false) literal in clauses.
    for s in symbols:
        found_pos, found_neg = False, False
        for c in clauses:
            if not found_pos and s in list_clauses('|', [c]):
                found_pos = True
            if not found_neg and ~s in list_clauses('|', [c]):
                found_neg = True
        if found_pos != found_neg:
            return s, found_pos
    return None, None

def Find_Unit_Clause(clauses, model):
    # Find a forced assignment from a clause with only 1 variable not bound in the model.
    for clause in clauses:
        P, value = None, None
        symbol,positive = None, None
        for literal in list_clauses('|', [clause]):
            if literal.op == '~':
                symbol, positive = literal.args[0], False
            if literal.op != '~':
                symbol, positive = literal, True
            # find a single variable/value pair that makes clause true in the model
            if symbol in model:
                if model[symbol] == positive:
                    P, value =  None, None # clause already True
            elif P:
                P, value = None, None # more than 1 unbound variable
            else:
                P, value = symbol, positive
        if P:
            return P, value
    return None, None
