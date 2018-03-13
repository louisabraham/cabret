import multiprocessing as mp

from tqdm import tqdm as _tqdm
from itertools import count


pool = None


def parallel_map(fun, args, proc=50):
    global pool
    if pool is None or proc > pool._processes:
        pool = mp.Pool(processes=proc)
    return pool.map(fun, args)


def tqdm(it, *args, cond=True, **kwargs):
    if it is None:
        it = count()
    if isinstance(it, int):
        it = range(it)
    if cond:
        return _tqdm(it, *args, **kwargs)
    else:
        return it
