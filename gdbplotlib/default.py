from .type_set import TypeSet
from . import std_types

default = TypeSet()
default.register(std_types.StdVector)
default.register(std_types.StdVectorBool)
default.register(std_types.StdArray)
default.register(std_types.Pointer)
default.register(std_types.Array)
default.register(std_types.Double)
default.register(std_types.Float)
default.register(std_types.StdComplexDouble)
default.register(std_types.StdComplexFloat)
default.register(std_types.Integral)
default.register(std_types.Bool)