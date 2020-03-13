from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

import gdb.types  # pylint: disable=E0401
import gdb  # pylint: disable=E0401
import numpy as np

from .type_set import TypeSet
from . import util


class TypeHandler(ABC):
    @staticmethod
    @abstractmethod
    def can_handle(gdb_type: gdb.Type) -> bool:
        """
        Returns whether the handler is able to extract values from a given type

        Parameters:
        gdb_type (gdb.Type): Type to be handled

        Returns:
        bool: Can the type be handled?
        """
        pass

    def __init__(self, type_set: TypeSet):
        self.type_set = type_set

    @abstractmethod
    def shape(self, gdb_value: gdb.Value) -> Tuple[Optional[int], ...]:
        """
        Gets the shape of a container

        Parameters:
        gdb_value (gdb.Value): The container

        Returns:
        Tuple[Optional[int]: The shape of the container. Any dimensions with
                             unbounded size are represented by None
        """
        pass

    @abstractmethod
    def contained_type(self, gdb_value: gdb.Value) -> Optional[gdb.Type]:
        """
        Gets the type of the elements of the container

        Parameters:
        gdb_value (gdb.Value): The container

        Returns:
        Optional[gdb.Type]: The element type. If the value is a scalar, and as
                            such does not hold elements, None is returned
        """
        pass

    @abstractmethod
    def extract(self, gdb_value: gdb.Value, index: Tuple[int, ...]):
        """
        Extracts a value from a GDB value

        Parameters:
        gdb_value (gdb.Value): GDB value
        index (Tuple[int, ...]): The multi-dimensional index of the value to
                                 extract

        Returns:
        value: The extracted value. Either a GDB value if gdb_value was a
               container, or a Numpy dtype if it was a scalar type
        """
        pass

    def extract_all(self, gdb_value: gdb.Value, slices: List[slice]):
        shape = self.shape(gdb_value)
        contained_type = self.contained_type(gdb_value)
        n_dims = len(shape)
        scalar_type = (contained_type == None)

        if scalar_type:
            return self.extract(gdb_value, None)

        basic_contained_type = gdb.types.get_basic_type(contained_type)
        contained_handler = self.type_set.get_handler(basic_contained_type)
        current_slices = slices[:n_dims]
        contained_slices = slices[n_dims:]

        for _ in range(len(shape) - len(current_slices)):
            current_slices.append(slice(None, None, None))

        def gen_output(slc, shp, index):
            if not shp:
                contained_gdb_value = self.extract(gdb_value, index)
                return contained_handler.extract_all(contained_gdb_value, contained_slices)
            else:
                out = []
                for i in util.indices_1d(slc[0], shp[0]):
                    out.append(gen_output(slc[1:], shp[1:], (*index, i)))

                return out

        out = gen_output(current_slices, shape, ())
        return out


class ScalarTypeHandler(TypeHandler):
    def shape(self, gdb_value: gdb.Value) -> Tuple[Optional[int], ...]:
        return ()

    def contained_type(self, gdb_value: gdb.Value) -> Optional[gdb.Type]:
        return None
