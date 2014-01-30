from . import structures

rm_dup = structures.Literal.remove_duplicates

def create_buckets(system):
    """Creates buckets from a given SAT problem."""
    buckets = [set() for x in range(0, system.nb_variables+1)]
    for clause in system:
        buckets[clause.max_literal().number].add(clause)
    return buckets

def extract_literal(literal_id, clause):
    """Returns two list, containing of instances of a literal, and all
    other literals."""
    equal = set()
    not_equal = set()
    for literal in clause:
        if literal.number == literal_id:
            equal.add(literal)
        else:
            not_equal.add(literal)
    return (equal, not_equal)

def resolve_bucket(bucket_id, buckets):
    """Returns possible resolutions for the given bucket."""
    clauses = set()
    for clause1 in buckets[bucket_id]:
        (equal1, not_equal1) = extract_literal(bucket_id, clause1)
        equal1 = rm_dup(equal1)
        assert len(equal1) >= 1, equal1
        for clause2 in buckets[bucket_id]:
            (equal2, not_equal2) = extract_literal(bucket_id, clause2)
            equal2 = rm_dup(equal2)
            assert len(equal2) >= 1, equal2
            if list(equal1)[0].polarity != list(equal2)[0].polarity:
                clause = structures.Clause(rm_dup(not_equal1 | not_equal2))
                clause.simplify()
                buckets[clause.max_literal().number].add(clause)

def solve(system):
    buckets = create_buckets(system)
    for i in range(len(buckets)-1, 0, -1):
        print(i)
        resolve_bucket(i, buckets)
    print(repr(buckets))
