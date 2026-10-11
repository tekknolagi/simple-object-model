import timeit
from objects import Class, OBJECT, TYPE, Instance, InstanceWithMap, MISSING

Point = Class(name="Point", base_class=OBJECT, fields={}, metaclass=TYPE)
P = Instance(Point)

def read_attr():
    P.read_attr("x")

P = InstanceWithMap(Point)
P.write_attr("x", 5)
P.write_attr("y", 6)
NO_MAP = object()
CACHED_MAP = P.map

class InlineCache:
    __slots__ = ("map", "idx")

    def __init__(self):
        self.map = NO_MAP
        self.idx = None

    def read(self, obj, fieldname):
        if obj.map is self.map:
            return obj.storage[self.idx]
        result = obj.read_attr(fieldname)
        if result is MISSING:
            return MISSING
        if obj.map is None:
            return result
        self.map = obj.map
        self.idx = obj.map.get_index(fieldname)
        return result

IC = InlineCache()

def read_attr_cached():
    IC.read(P, "x")

if __name__ == '__main__':
    t, *_ = timeit.repeat(read_attr, number=10_000_000, repeat=1)
    print(f"Without cache: {t:.2}s")
    t, *_ = timeit.repeat(read_attr_cached, number=10_000_000, repeat=1)
    print(f"With cache: {t:.2}s")
