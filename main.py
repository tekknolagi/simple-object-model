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
        super().__init__(cls, {})

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

if __name__ == '__main__':
    unittest.main()
