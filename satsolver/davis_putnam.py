from . import structures

def create_buckets(system):
    """Creates buckets from a given SAT problem."""
    buckets = [set() for x in range(0, system.nb_variables+1)]
    for clause in system:
        buckets[abs(clause.max_literal())].add(clause)
    return buckets

def extract_literal(literal_id, clause):
    """Returns two list, containing of instances of a literal, and all
    other literals."""
    variations = set([literal_id, -literal_id])
    equal = variations & clause.literals
    not_equal = clause.literals - variations
    return (equal, not_equal)

def resolve_bucket(bucket_id, buckets):
    """Returns possible resolutions for the given bucket."""
    clauses = set()
    for clause1 in buckets[bucket_id]:
        (equal1, not_equal1) = extract_literal(bucket_id, clause1)
        assert len(equal1) >= 1, equal1
        for clause2 in buckets[bucket_id]:
            (equal2, not_equal2) = extract_literal(bucket_id, clause2)
            assert len(equal2) >= 1, equal2
            if list(equal1)[0] != list(equal2)[0]:
                # Equivalent to polarity comparison
                clause = structures.Clause(not_equal1 | not_equal2)
                buckets[abs(clause.max_literal())].add(clause)

def solve(system):
    buckets = create_buckets(system)
    for i in range(len(buckets)-1, 0, -1):
        print(i)
        resolve_bucket(i, buckets)
    print(repr(buckets))
