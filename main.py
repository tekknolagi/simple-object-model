# Based on CF Bolz-Tereick's https://aosabook.org/en/500L/a-simple-object-model.html
import unittest

class Base:
    def __init__(self, cls, fields):
        self.cls = cls
        self._fields = fields

    def read_attr(self, fieldname):
        return self._read_dict(fieldname)

    def write_attr(self, fieldname, value):
        return self._write_dict(fieldname, value)

    def isinstance(self, cls):
        return self.cls.issubclass(cls)

    def callmethod(self, methname, *args):
        meth = self.cls._read_from_class(methname)
        return meth(self, *args)

    def _read_dict(self, fieldname):
        return self._fields.get(fieldname, MISSING)

    def _write_dict(self, fieldname, value):
        self._fields[fieldname] = value

MISSING = object()

class Instance(Base):
    def __init__(self, cls: Class):
        super().__init__(cls, None)
        self.map = EMPTY_MAP
        self.storage = []

    def _read_dict(self, fieldname):
        index = self.map.get_index(fieldname)
        if index == -1:
            return MISSING
        return self.storage[index]

    def _write_dict(self, fieldname, value):
        index = self.map.get_index(fieldname)
        if index != -1:
            self.storage[index] = value
        else:
            new_map = self.map.next_map(fieldname)
            self.storage.append(value)
            self.map = new_map

class Class(Base):
    def __init__(self, name, base_class, fields, metaclass):
        super().__init__(metaclass, fields)
        self.name = name
        self.base_class = base_class

    def method_resolution_order(self):
        if self.base_class is None:
            return [self]
        return [self] + self.base_class.method_resolution_order()

    def issubclass(self, cls):
        return cls in self.method_resolution_order()

OBJECT = Class(name="object", base_class=None, fields={}, metaclass=None)
TYPE = Class(name="type", base_class=OBJECT, fields={}, metaclass=None)
TYPE.cls = TYPE
OBJECT.cls = TYPE

class Map:
    def __init__(self, attrs):
        self.attrs = attrs
        self.next_maps = {}

    def get_index(self, fieldname):
        return self.attrs.get(fieldname, -1)

    def next_map(self, fieldname):
        assert fieldname not in self.attrs
        if fieldname in self.next_maps:
            return self.next_maps[fieldname]
        attrs = self.attrs.copy()
        attrs[fieldname] = len(attrs)
        result = self.next_maps[fieldname] = Map(attrs)
        return result

EMPTY_MAP = Map({})

class Tests(unittest.TestCase):
    def test_read_write_field(self):
        A = Class(name="A", base_class=OBJECT, fields={}, metaclass=TYPE)
        obj = Instance(A)
        obj.write_attr("a", 1)
        self.assertEqual(obj.read_attr("a"), 1)

        obj.write_attr("b", 5)
        self.assertEqual(obj.read_attr("a"), 1)
        self.assertEqual(obj.read_attr("b"), 5)

        obj.write_attr("a", 2)
        self.assertEqual(obj.read_attr("a"), 2)
        self.assertEqual(obj.read_attr("b"), 5)

    def test_read_write_field_class(self):
        A = Class(name="A", base_class=OBJECT, fields={"a": 1}, metaclass=TYPE)
        self.assertEqual(A.read_attr("a"), 1)
        A.write_attr("a", 5)
        self.assertEqual(A.read_attr("a"), 5)

    def test_isinstance(self):
        A = Class(name="A", base_class=OBJECT, fields={}, metaclass=TYPE)
        B = Class(name="B", base_class=A, fields={}, metaclass=TYPE)
        b = Instance(B)
        self.assertTrue(b.isinstance(B))
        self.assertTrue(b.isinstance(A))
        self.assertTrue(b.isinstance(OBJECT))
        self.assertFalse(b.isinstance(TYPE))

    def test_maps(self):
        Point = Class(name="Point", base_class=OBJECT, fields={}, metaclass=TYPE)
        p1 = Instance(Point)
        p1.write_attr("x", 1)
        p1.write_attr("y", 2)
        self.assertEqual(p1.storage, [1, 2])
        self.assertEqual(p1.map.attrs, {"x": 0, "y": 1})

        p2 = Instance(Point)
        p2.write_attr("x", 5)
        p2.write_attr("y", 6)
        self.assertIs(p1.map, p2.map)
        self.assertEqual(p2.storage, [5, 6])

        p1.write_attr("x", -1)
        p1.write_attr("y", -2)
        self.assertIs(p1.map, p2.map)
        self.assertEqual(p1.storage, [-1, -2])

        p3 = Instance(Point)
        p3.write_attr("x", 100)
        p3.write_attr("z", -343)
        self.assertIsNot(p3.map, p1.map)
        self.assertEqual(p3.map.attrs, {"x": 0, "z": 1})

    def test_different_class_has_same_map(self):
        Point = Class(name="Point", base_class=OBJECT, fields={}, metaclass=TYPE)
        p = Instance(Point)
        p.write_attr("x", 1)
        p.write_attr("y", 2)
        self.assertEqual(p.map.attrs, {"x": 0, "y": 1})

        Vec2 = Class(name="Vec2", base_class=OBJECT, fields={}, metaclass=TYPE)

        v = Instance(Vec2)
        v.write_attr("x", 5)
        v.write_attr("y", 6)
        self.assertIs(p.map, v.map)

if __name__ == '__main__':
    unittest.main()
