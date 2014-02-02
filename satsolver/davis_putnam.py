from . import structures

class NotSatisfiable(Exception):
    pass
class UnknownSatisfiability(Exception):
    pass

def create_buckets(system):
    """Creates buckets from a given SAT problem."""
    buckets = [set() for x in range(0, system.nb_variables+1)]
    for clause in system:
        buckets[abs(clause.max_literal())].add(clause)
    return buckets

def resolve_bucket(bucket_id, buckets, verbose):
    """Returns possible resolutions for the given bucket."""
    bucket = list(buckets[bucket_id])
    with_literal = list(filter(lambda x:bucket_id in x, bucket))
    with_negative_literal = list(filter(lambda x:-bucket_id in x, bucket))
    for (i, clause1) in enumerate(with_literal):
        # Iteration over clauses with positive occurence of the biggest
        # literal
        for clause2 in with_negative_literal:
            # Iteration over clauses with negative occurence of the biggest
            # literal

            clause = (clause1 | clause2).strip_variable(bucket_id)
            # Resolution
            index = abs(clause.max_literal())
            # Index of the bucket we will put the clause in
            assert index != bucket_id
            if len(clause) == 1:
                literal = list(clause)[0]
                buckets[index] = set([clause] +
                        list(filter(lambda x:-literal in x, buckets[index])))
                # Removing all clauses containing this one
                return
            elif not clause.always_satisfied:
                buckets[index].add(clause)

def solve(system, verbose=False):
    buckets = create_buckets(system)
    for i in range(len(buckets)-1, 0, -1):
        if verbose:
            print('%i %i' % (i, len(buckets[i])))
        resolve_bucket(i, buckets, verbose)
    valuation = [None]
    for (i, bucket) in enumerate(buckets):
        if i != 0:
            exists_false = False
            exists_true = False
            for clause in bucket:
                if i in clause and -i in clause or \
                        clause.strip_variable(i).is_satisfied(valuation):
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
