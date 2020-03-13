import pickle

import gdb  # pylint: disable=E0401

from . import data_extractor
from . import util

try:
    import scipy.io
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False


class SaveMat(gdb.Command):
    def __init__(self):
        super(SaveMat, self).__init__("savemat", gdb.COMMAND_OBSCURE)

    def invoke(self, args, from_tty):
        if not SCIPY_AVAILABLE:
            raise RuntimeError("Scipy not available")

        out = {}
        filename, var = args.split()

        for v in var:
            data = data_extractor.extract_var(v)
            base_var, _ = util.split_variable_and_slice(v)
            dict_name = util.strip_non_alphanumeric(base_var)
            out[dict_name] = data

        scipy.io.savemat(filename, out)


class SavePy(gdb.Command):
    def __init__(self):
        super(SavePy, self).__init__("savepy", gdb.COMMAND_OBSCURE)

    def invoke(self, args, from_tty):
        filename, var = args.split()
        data = data_extractor.extract_var(var)
        with open(filename, "wb") as file:
            pickle.dump(data, file)


class Save(gdb.Command):
    def __init__(self):
        super(Save, self).__init__("save", gdb.COMMAND_OBSCURE)

    def invoke(self, args, from_tty):
        filename, var = args.split()
        data = data_extractor.extract_var(var)
        data.tofile(filename)


SaveMat()
SavePy()
Save()