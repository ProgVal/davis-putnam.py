class Clause(frozenset):
    __slots__ = ()
    def __str__(self):
        return ' '.join(map(str, self)) + ' 0'

    def __repr__(self):
        return 'Clause(%r)' % super(Clause, self).__repr__()

    def __or__(self, other):
        """Union"""
        if any(map(lambda x:(not x) in other, self)):
            return Clause(set())
        return Clause(super(Clause, self).__or__(other))

    def max_literal(self):
        if self:
            return max(self, key=abs)
        else:
            return 0

    def strip_variable(self, i):
        """Returns a clause with all instances of a literal and its negation
        removed."""
        return Clause(self - set([i, -i]))

    @property
    def always_satisfied(self):
        if len(self) != 2:
            return False
        else:
            literals = list(self)
            return literals[0] == -literals[1]

    def is_satisfied(self, valuation):
        return any(map(lambda x:(x>0) is valuation[abs(x)], self))
            

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
