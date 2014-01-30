import collections

from . import structures

def parse(fd):
    nb_variables = None
    nb_clauses = None
    clauses = []
    for line in fd.readlines():
        line = line[0:-1] # Strip line ending character
        tokens = list(filter(bool, line.split(' '))) # Eliminate empty tokens
        if not tokens or tokens[0] == 'c':
            continue
        elif tokens[0] == 'p':
            assert len(tokens) == 4
            assert tokens[1] == 'cnf'
            assert nb_variables is None and nb_clauses is None, \
                    'Duplicate header'
            (nb_variables, nb_clauses) = tokens[2:]
        else:
            assert nb_variables is not None and nb_clauses is not None, \
                    'Missing header'
            assert tokens[-1] == '0'
            literals = map(int, tokens[0:-1])
            clauses.append(structures.Clause(literals))
    return structures.System(int(nb_variables), clauses)
