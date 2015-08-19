from enum import IntEnum

class Granularity(IntEnum):
    METHOD = 0
    CLASS = 1
    FUNCTION = 2
    PACKAGE = 3
    SOFTWARE = 4

    def parent(self):
        if self == type(self).CLASS:
            return type(self).PACKAGE
        elif self == type(self).SOFTWARE:
            return self

        return Granularity(self.value + 1)

    # FYI: __cmp__ was deprecated on Python 3 and this should be implemented by using __lt__ and __eq__ on it
    def __cmp__(self, other):
        if (self.value in [type(self).METHOD.value, type(self).CLASS.value] and other.value is type(self).FUNCTION.value) or (other.value in [type(self).METHOD.value, type(self).CLASS.value] and self.value is type(self).FUNCTION.value):
            raise ValueError("Undefined comparison between CLASS or METHOD and FUNCTION")

        return super(Granularity, self).__cmp__(other)

    def __str__(self):
        return self.name
