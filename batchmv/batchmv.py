import os
import itertools


class UnsafeBatchRenameError(Exception):
    pass


def batch_rename_issafe(AtoB) -> None:
    """
    :param AtoB: A->B is a bijective mapping such that
           {(a_i, b_i) | 1 <= i <= n}
    return: True if no conflict/overwriting will take place;
            False otherwise
    :raise UnsafeBatchRenameError: if AtoB is not bijective, and/or
           overwriting may happen when renaming

    >>> batch_rename_issafe([])
    >>> batch_rename_issafe([('a', 'b')])
    >>> batch_rename_issafe([('a', 'a')])
    >>> batch_rename_issafe([('a', 'a'), ('b', 'b')])
    >>> try:
    ...     batch_rename_issafe([('a', 'b'), ('b', 'c')])
    ... except UnsafeBatchRenameError:
    ...     pass
    ... else:
    ...     assert False
    >>> batch_rename_issafe([('b', 'c'), ('a', 'b')])
    """
    AtoB = list(filter(lambda x: x[0] != x[1], AtoB))
    A = [x[0] for x in AtoB]
    B = [x[1] for x in AtoB]
    if len(A) > len(set(A)) or len(B) > len(set(B)):
        raise UnsafeBatchRenameError

    for i, (_, b) in enumerate(AtoB):
        Aremain = (x[0] for x in AtoB[i + 1:])
        if b in Aremain:
            raise UnsafeBatchRenameError


def brename_bf(AtoB) -> None:
    """
    Try all possible renaming permutation until finding one without confict.

    :param AtoB: a list of tuples (from_filename, to_filename)
    :raise UnsafeBatchRenameError: to avoid overwriting any file, you must
           ``touch`` some temporary files, it seems if this error is raised
    """
    for AtoB_i in itertools.permutations(AtoB):
        try:
            batch_rename_issafe(list(AtoB_i))
        except UnsafeBatchRenameError:
            pass
        else:
            for ffilename, tfilename in AtoB_i:
                if ffilename != tfilename:
                    os.rename(ffilename, tfilename)
            return
    raise UnsafeBatchRenameError
