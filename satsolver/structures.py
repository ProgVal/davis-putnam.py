class Clause(frozenset):
    """A subclasses of frozenset (ie. unmutable set) that implements extra
    methods for computing clauses properties and operations."""
    __slots__ = ()
    def __str__(self):
        return ' '.join(map(str, self)) + ' 0'

    def __or__(self, other):
        """Union of two clauses."""
        if any(map(lambda x:(not x) in other, self)):
            return Clause(set())
        return Clause(super(Clause, self).__or__(other))

    def max_literal(self):
        """Returns the maximum literal of the clauses, using the absolute
        value for ordering."""
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
        """Determines whether or not a clause is always satisfied."""
        if len(self) != 2:
            return False
        else:
            literals = list(self)
            return literals[0] == -literals[1]

    def is_satisfied(self, valuation):
        """Determines whether or not a clause is satisfied for the given
        valuation."""
        return any(map(lambda x:(x>0) is valuation[abs(x)], self))

class System:
    """Represents a set of clauses, with extra data provided by the cnf file
    header."""
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
