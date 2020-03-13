import re
from typing import List

import gdb  # pylint: disable=E0401
import gdb.types  # pylint: disable=E0401
import numpy as np

from .default import default
from .type_set import TypeSet
from . import util


class SliceSyntaxError(Exception):
    pass


class VariableError(Exception):
    pass


def parse_subslice(subslice: str) -> slice:
    slice_components = subslice.split(":")

    try:
        s = [int(gdb.parse_and_eval(x)) if x else None for x in slice_components]
    except (ValueError, gdb.error):
        raise SliceSyntaxError(f"Invalid slice component: {subslice}")

    if len(s) == 1:
        return slice(s[0], s[0] + 1)
    if len(s) == 2:
        return slice(s[0], s[1])
    elif len(s) == 3:
        return slice(s[0], s[1], s[2])
    else:
        raise SliceSyntaxError(f"Invalid slice component: {subslice}")


def parse_slice(full_slice: str) -> List[slice]:
    slice_dims = full_slice.split(",")
    return [parse_subslice(s) for s in slice_dims]


def parse_var(var: str):
    var_base, slice_str = util.split_variable_and_slice(var)
    slices = parse_slice(slice_str) if slice_str else []
    return var_base, slices


def extract_var(var: str, type_set: TypeSet = default) -> np.ndarray:
    base_var, var_slice = parse_var(var)

    try:
        gdb_data = gdb.parse_and_eval(base_var)
    except gdb.error:
        raise VariableError(f"Invalid variable: {var}")

    gdb_type = gdb.types.get_basic_type(gdb_data.type)
    type_handler = type_set.get_handler(gdb_type)

    out = type_handler.extract_all(gdb_data, var_slice)
    out_np = np.squeeze(np.array(out))
    return out_np
