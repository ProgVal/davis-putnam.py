class Clause:
    __slots__ = ('literals',)
    def __init__(self, literals):
        self.literals = set(literals)

    def __contains__(self, v):
        return v in self.literals

    def __iter__(self):
        return iter(self.literals)

    def __str__(self):
        return ' '.join(map(str, self)) + ' 0'

    def __repr__(self):
        return 'Clause(%r)' % self.literals

    def __or__(self, other):
        """Union"""
        if any(lambda x:(not x) in other, self):
            return Clause(set())
        return Clause(self.literals | other.literals)

    def max_literal(self):
        if self.literals:
            return max(self.literals, key=abs)
        else:
            return 0

    def simplify(self):
        literals = set()
        for literal in self.literals:
            if -int(literal) in literals:
                self.literals = set([literal, -literal])
                return
            else:
                literals.add(int(literal))
        self.literals = set(literals)
            

    @classmethod
    def remove_duplicates(cls, clauses):
        new_clauses = set()
        for clause1 in clauses:
            for clause2 in new_clauses:
                if clause1 == clause2:
                    break
            else:
                new_clauses.add(clause1)
        return new_clauses

class System:
    __slots__ = ('nb_variables', 'clauses')
    def __init__(self, nb_variables, clauses):
        self.nb_variables = nb_variables
        self.clauses = set(clauses)

    def __iter__(self):
        return iter(self.clauses)

    def __str__(self):
        return '\n'.join(map(str, self))

    def __repr__(self):
        return 'System(%r)' % self.clauses

    def __or__(self, other):
        """Union"""
        return System(self.clauses | other.clauses)

    def max_literal(self):
        return Clause.max(self.clauses)
