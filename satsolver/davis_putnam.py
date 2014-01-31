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
    return clause.literals - set([literal_id, -literal_id])

def resolve_bucket(bucket_id, buckets):
    """Returns possible resolutions for the given bucket."""
    bucket = list(buckets[bucket_id])
    with_literal = list(filter(lambda x:bucket_id in x, bucket))
    with_negative_literal = list(filter(lambda x:-bucket_id in x, bucket))
    for (i, clause1) in enumerate(with_literal):
        print('%i %i' % (len(with_literal), i))
        not_equal1 = extract_literal(bucket_id, clause1)
        for clause2 in with_negative_literal:
            not_equal2 = extract_literal(bucket_id, clause2)
            clause = structures.Clause(not_equal1 | not_equal2)
            index = abs(clause.max_literal())
            assert index != bucket_id
            buckets[index].add(clause)

def solve(system):
    buckets = create_buckets(system)
    for i in range(len(buckets)-1, 0, -1):
        print('%i %i' % (i, len(buckets[i])))
        resolve_bucket(i, buckets)
    valuation = [None]
    for (i, bucket) in enumerate(buckets):
        if i == 0 and bucket:
            # No solution
            return None
        elif i != 0:
            exists_false = False
            exists_true = False
            for clause in bucket:
                if i in clause and -i in clause:
                    # Clause is always satisfied
                    pass
                elif i in clause:
                    exists_true = True
                else:
                    assert -i in clause, ('Clause in bucket %i containing '
                            'neither %i or -%i') % (i, i, i)
                    exists_false = True
            if exists_true:
                valuation.append(True)
            elif exists_false:
                valuation.append(False)
            else:
                # All clauses are always satisfied
                valuation.append(True)
    return valuation
