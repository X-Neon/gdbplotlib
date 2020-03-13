import re
from typing import List, Tuple, Optional


def indices_1d(s: slice, shape: int):
    if shape is None:
        start = 0 if s.start is None else s.start
        stop = 0 if s.stop is None else s.stop
        step = 1 if s.step is None else s.step
    else:
        start, stop, step = s.indices(shape)

    in_range = lambda a, b, c: a < b if c > 0 else a > b
    i = start
    while in_range(i, stop, step):
        yield i
        i += step


def indices(slices: List[slice], shape: Tuple):
    if len(slices) != len(shape):
        for i in range(len(shape) - len(slices)):
            slices.append(slice(None, None, None))


    if len(slices) == 1:
        for i in indices_1d(slices[0], shape[0]):
            yield (i,)
    else:
        for i in indices_1d(slices[0], shape[0]):
            for j in indices(slices[1:], shape[1:]):
                yield (i, *j)


def split_variable_and_slice(var: str) -> Tuple[str, Optional[str]]:
    lbracket = var.rfind("[")
    rbracket = var.rfind("]")

    if lbracket == -1 or rbracket == -1:
        return var, None
    else:
        return var[:lbracket], var[lbracket+1:rbracket]


def strip_non_alphanumeric(s: str) -> str:
    return re.sub("\\W+", "", s)