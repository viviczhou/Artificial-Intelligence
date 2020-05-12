'''
Project #2 Automated Reasoning
Version 2.0 created at 2019/10/23
    useful tools used in implementation of algorithms
'''

from collections import defaultdict

class Expr(object):
    """op: str; args: Expressions."""
    def __init__(self, op, *args):
        self.op = str(op)
        self.args = args

    def __and__(self, rhs):
        return Expr('&', self, rhs)

    def __or__(self, rhs):
        # for P | Q:
        if isinstance(rhs, Expr):
            return Expr('|', self, rhs)
        # for P |'==>'| Q:
        else:
            return Partition(rhs, self)

    def __invert__(self):
        return Expr('~', self)

    def __eq__(self, other):
        return (isinstance(other, Expr)
                and self.op == other.op
                and self.args == other.args)

    def __hash__(self):
        return hash(self.op) ^ hash(self.args)

    def __call__(self, *args):
        if self.args:
            raise ValueError
        else:
            return Expr(self.op, *args)

class Partition:
    def __init__(self, op, lhs):
        self.op = op
        self.lhs = lhs

    def __or__(self, rhs):
        return Expr(self.op, self.lhs, rhs)

class keydict(defaultdict):
    # default_factory is a function of the key (different from defaultdict)
    def __missing__(self, key):
        self[key] = self.default_factory(key)
        return self[key]

def expr(x):
    # identifiers are automatically defined as Symbols.
    if isinstance(x, str):
        def Symbol(name):
            # Expr with no args
            return Expr(name)
        def handle_infix(x):
            # replace ==> |'==>'|
            for op in ['==>', '<=>']:
                x = x.replace(op, '|' + repr(op) + '|')
            return x
        # treat ==>, <==, and <=> as infix |'==>'|, |'<=='|, and |'<=>'|.
        return eval(handle_infix(x), keydict(Symbol))
    else:
        # not change expression: expr('P & Q ==> Q') return ((P & Q) ==> Q)
        return x

def first(iterable, default=None):
    try: # return the first element of an iterable
        return iterable[0]
    except IndexError: # or return defualt
        return default
    except TypeError: # or return the next element of a generator
        return next(iterable, default)

def combine_cluases(op, args):
    clauses = list_clauses(op, args)
    if len(clauses) == 0:
        return {'&': True, '|': False}[op]
    elif len(clauses) == 1:
        return clauses[0]
    else:
        return Expr(op, *clauses)

def list_clauses(op, args):
    # return a list of clauses
    clauses = []
    def collect(clause):
        for arg in clause:
            if arg.op == op:
                collect(arg.args)
            else:
                clauses.append(arg)
    collect(args)
    return clauses

def toCNF(sentence):
    initial = expr(sentence)
    step1_2 = eliminate_implications(initial)  # Steps 1, 2
    step_3 = move_not_inwards(step1_2)  # Step 3
    cnf = distribute_and_over_or(step_3) # Step 4
    return cnf

def eliminate_implications(s):
    if not s.args or (isinstance(s.op, str) and s.op[:1].isalpha()):
        return s  # Atoms are unchanged.
    args = list(map(eliminate_implications, s.args)) # remove all implications [lhs1,[lhs2[[lh3[...]]]]]
    lhs, rhs = args[0], args[-1] # do it layer by layer
    if s.op == '==>':
        return rhs | ~lhs
    elif s.op == '<=>':
        return (~lhs | rhs) & (~rhs | lhs)
    else:
        return Expr(s.op, *args)

def move_not_inwards(s):
    if s.op == '~':
        child = s.args[0]
        def NOT(arg):
            return move_not_inwards(~arg)
        if child.op == '~':
            return move_not_inwards(child.args[0])  # ~~A ==> A
        if child.op == '&':
            return combine_cluases('|', list(map(NOT, child.args))) # ~ (A & B) = (~A | ~B) and check each layer
        if child.op == '|':
            return combine_cluases('&', list(map(NOT, child.args))) # ~ (A | B) = (~A & ~B) and check each layer
        return s
    elif (isinstance(s.op, str) and s.op[:1].isalpha()) or not s.args:
        return s # atoms not changed
    else:
        return Expr(s.op, *list(map(move_not_inwards, s.args))) # check layer by layer

def distribute_and_over_or(s):
    if s.op == '|':
        set_s = combine_cluases('|', s.args)
        if set_s.op != '|':
            return distribute_and_over_or(set_s)
        if len(set_s.args) == 0:
            return False # symbol
        if len(set_s.args) == 1:
            return distribute_and_over_or(set_s.args[0]) # any layer inside?
        conjunction = None
        for arg in set_s.args:
            if arg.op == '&':
                conjunction = first([arg], None)
        if not conjunction:
            return set_s
        unconjuncts = []
        for arg in set_s.args:
            if arg is not conjunction:
                unconjuncts.append(arg)
        left_out = combine_cluases('|', unconjuncts)
        cnf = []
        for arg in conjunction.args:
            new_clause = distribute_and_over_or(arg|left_out)
            cnf.append(new_clause)
        return combine_cluases('&', cnf)
    elif s.op == '&':
        return combine_cluases('&', list(map(distribute_and_over_or, s.args)))
    else:
        return s
