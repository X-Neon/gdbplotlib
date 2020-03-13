class UnkownTypeError(Exception):
    pass


class TypeSet:
    def __init__(self):
        self.handlers = []

    def register(self, type_handler):
        self.handlers.append(type_handler)

    def get_handler(self, gdb_type):
        for handler in self.handlers:
            if handler.can_handle(gdb_type):
                return handler(self)

        raise UnkownTypeError(f"Cannot handle type: {str(gdb_type)}")
