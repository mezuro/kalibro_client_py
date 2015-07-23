from enum import IntEnum

class Granularity(IntEnum):
    METHOD = 0
    CLASS = 1
    PACKAGE = 2
    SOFTWARE = 3

    def parent(self):
        if self == type(self).SOFTWARE:
            return self

        return Granularity(self.value + 1)

    def __str__(self):
        return self.name
