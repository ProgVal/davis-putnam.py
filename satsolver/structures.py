class Literal:
    __slots__ = ('polarity', 'number')
    def __init__(self, polarity, number):
        self.polarity = polarity
        self.number = number

    @classmethod
    def from_string(cls, s):
        if s.startswith('-'):
            return cls(False, int(s[1:]))
        else:
            return cls(True, int(s))

    def __str__(self):
        return '%s%i' % (('' if self.polarity else '-'), self.number)

    def __repr__(self):
        return 'Literal(%r, %i)' % (self.polarity, self.number)

    def __eq__(self, other):
        return int(self) == int(other)

    @classmethod
    def max(cls, list_):
        max_ = Literal(True, 0)
        for literal in list_:
            if literal.number > max_.number:
                max_ = literal
        return max_

    @classmethod
    def from_int(cls, i):
        return cls(i >= 0, abs(i))

    def __int__(self):
        """Prevents sets from containing twice the same literal."""
        return (+1 if self.polarity else -1) * self.number

    def __hash__(self):
        return int(self)

    @classmethod
    def remove_duplicates(cls, literals):
        int_set = set(map(int, literals))
        return set(map(Literal.from_int, int_set))

    def oposite(self):
        return Literal(not self.polarity, self.number)

class Clause:
    __slots__ = ('literals',)
    def __init__(self, literals):
        self.literals = set(literals)

    def __contains__(self, v):
        if isinstance(v, int):
            return any(lambda x:int(x)==v, self.literals)
        elif isinstance(v, Literal):
            return v in self.literals
        else:
            raise AssertionError(v.__class__.__name__)

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
        return Literal.max(self.literals)

    def simplify(self):
        literals = set()
        for literal in self.literals:
            if -int(literal) in literals:
                self.literals = set([literal, literal.oposite()])
                return
            else:
                literals.add(int(literal))
        self.literals = set(map(Literal.from_int, literals))
            

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
