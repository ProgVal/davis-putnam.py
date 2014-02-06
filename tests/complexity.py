#!/usr/bin/env python3

import sys
import random
import itertools

def get_tests(n):
    if n == 1:
        return [{-1}, {1}]
    else:
        clauses = get_tests(n-1)
        return list(itertools.chain(*map(lambda c:(c | {-n}, c | {n}), clauses)))

if len(sys.argv) != 2 or not sys.argv[1].isnumeric:
    printf('Syntax: %s n' % sys.argv[0])
    exit()

n = int(sys.argv[1])

clauses = get_tests(n)

removed_clause = random.choice(clauses)
clauses.remove(removed_clause)


print('p cnf %i %i' % (n, len(clauses)))
for clause in clauses:
    print(' '.join(map(str, clause)) + ' 0')

result = ' '.join(map(lambda i:str(-i), sorted(removed_clause, key=abs)))
# Writing to stderr in order not to get it piped to the solver
sys.stderr.write('c The unique solution is: %s\n' % result)
