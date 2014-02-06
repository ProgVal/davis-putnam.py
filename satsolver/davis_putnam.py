from . import structures

class NotSatisfiable(Exception):
    pass
class UnknownSatisfiability(Exception):
    pass

def create_buckets(system):
    """Creates buckets from a given SAT problem."""
    buckets = [set() for x in range(0, system.nb_variables+1)]
    for clause in system:
        buckets[clause.max_literal()].add(clause)
    return buckets

def simplify_buckets(buckets, up_to):
    for (i, bucket1) in enumerate(buckets[1:up_to]):
        for clause in bucket1:
            pred = lambda x:clause is x or not clause.issubset(x)
            for j in range(up_to, i, -1):
                bucket2 = buckets[j]
                assert all(map(lambda x:x.max_literal()==j, bucket2)),\
                        (j, bucket2)
                new_bucket = set(filter(pred, bucket2))
                assert all(map(lambda x:x.max_literal()==j, new_bucket)),\
                        (j, new_bucket)
                buckets[j] = new_bucket

def resolve_bucket(bucket_id, buckets):
    """Returns possible resolutions for the given bucket."""
    bucket = list(buckets[bucket_id])
    if REMOVE_TAUTOLOGIES:
        bucket = list(filter(lambda x:not x.always_satisfied, bucket))
    with_literal = filter(lambda x:bucket_id in x, bucket)
    with_negative_literal = list(filter(lambda x:-bucket_id in x, bucket))
    for (i, clause1) in enumerate(with_literal):
        # Iteration over clauses with positive occurence of the biggest
        # literal
        for clause2 in with_negative_literal:
            # Iteration over clauses with negative occurence of the biggest
            # literal

            clause = clause1.strip_variable(bucket_id) | \
                    clause2.strip_variable(-bucket_id)
            # Resolution
            index = clause.max_literal()
            # Index of the bucket we will put the clause in
            if not REMOVE_TAUTOLOGIES or not clause.always_satisfied:
                buckets[index].add(clause)
    if REMOVE_DUPLICATES:
        simplify_buckets(buckets, bucket_id)

def solve(system):
    buckets = create_buckets(system)
    for i in range(len(buckets)-1, 0, -1):
        if VERBOSE:
            print('%i %r' % (i, list(map(len, buckets))))
        resolve_bucket(i, buckets)
    valuation = []
    for (i, bucket) in enumerate(buckets):
        assert len(valuation) == i
        if i == 0:
            valuation.append(None)
        else:
            exists_false = False
            exists_true = False
            for clause in bucket:
                if i in clause and -i in clause or \
                        clause.strip_variable(i).strip_variable(-i)\
                        .is_satisfied(valuation):
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
                for clause2 in bucket:
                    if not clause2.is_satisfied(valuation):
                        raise NotSatisfiable()
            elif exists_false:
                valuation.append(False)
                for clause2 in bucket:
                    if not clause2.is_satisfied(valuation):
                        raise NotSatisfiable()
            else:
                # All clauses are always satisfied
                valuation.append(True)
    return valuation
