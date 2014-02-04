try:
    import multiprocessing
    PROCESSES = 4
    def immediate_exit(f):
        """Decorator for function that will be called in another process
        to abord all process if a KeyboardInterrupt (ie. Ctrl-C) is sent."""
        def newf(*args, **kwargs):
            try:
                f(*args, **kwargs)
            except KeyboardInterrupt:
                exit()
        return newf
except ImportError:
    pass
import functools

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

def divide_into_chunks(clauses):
    """Divides a list of clauses into several chunks to process them
    in multiple threads."""
    chunks = []
    chunk_size = int(len(with_literal)/PROCESSES/4)
    for i in range(0, PROCESSES):
        chunks.append(clauses[i*chunk_size:(i+1)*chunk_size])
    chunks.append(clauses[PROCESSES*chunk_size:])
    return chunks

def resolve_bucket(bucket_id, buckets, verbose, multiprocess):
    """Returns possible resolutions for the given bucket."""
    bucket = list(buckets[bucket_id])
    with_literal = list(filter(lambda x:bucket_id in x, bucket))
    with_negative_literal = list(filter(lambda x:-bucket_id in x, bucket))
    if multiprocess:
        pool = multiprocessing.Pool(PROCESSES)
        worker = functools.partial(merge_clauses,
                bucket_id, with_literal, verbose=verbose)
        chunks = divide_into_chunks(with_negative_literal)
        for new_buckets in pool.map(worker, chunks):
            for (i, new_bucket) in enumerate(new_buckets):
                buckets[i] |= new_bucket
    else:
        new_buckets = merge_clauses(bucket_id, with_literal,
                with_negative_literal, verbose)
        for (i, new_bucket) in enumerate(new_buckets):
            buckets[i] |= new_bucket


def merge_clauses(bucket_id, with_literal, with_negative_literal, verbose):
    new_buckets = [set() for x in range(0, bucket_id)]
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
            if not clause.always_satisfied:
                new_buckets[index].add(clause)
    return new_buckets

def solve(system, verbose=False, multiprocess=False):
    buckets = create_buckets(system)
    for i in range(len(buckets)-1, 0, -1):
        if verbose:
            print('%i %i' % (i, len(buckets[i])))
        resolve_bucket(i, buckets, verbose, multiprocess)
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
