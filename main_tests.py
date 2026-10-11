import unittest
from main import Class, OBJECT, TYPE, Instance, InstanceWithMap

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

    def test_maps(self):
        Point = Class(name="Point", base_class=OBJECT, fields={}, metaclass=TYPE)
        p1 = InstanceWithMap(Point)
        p1.write_attr("x", 1)
        p1.write_attr("y", 2)
        self.assertEqual(p1.storage, [1, 2])
        self.assertEqual(p1.map.attrs, {"x": 0, "y": 1})

        p2 = InstanceWithMap(Point)
        p2.write_attr("x", 5)
        p2.write_attr("y", 6)
        self.assertIs(p1.map, p2.map)
        self.assertEqual(p2.storage, [5, 6])

        p1.write_attr("x", -1)
        p1.write_attr("y", -2)
        self.assertIs(p1.map, p2.map)
        self.assertEqual(p1.storage, [-1, -2])

        p3 = InstanceWithMap(Point)
        p3.write_attr("x", 100)
        p3.write_attr("z", -343)
        self.assertIsNot(p3.map, p1.map)
        self.assertEqual(p3.map.attrs, {"x": 0, "z": 1})

    def test_different_class_has_same_map(self):
        Point = Class(name="Point", base_class=OBJECT, fields={}, metaclass=TYPE)
        p = InstanceWithMap(Point)
        p.write_attr("x", 1)
        p.write_attr("y", 2)
        self.assertEqual(p.map.attrs, {"x": 0, "y": 1})

        Vec2 = Class(name="Vec2", base_class=OBJECT, fields={}, metaclass=TYPE)

        v = InstanceWithMap(Vec2)
        v.write_attr("x", 5)
        v.write_attr("y", 6)
        self.assertIs(p.map, v.map)

if __name__ == '__main__':
    unittest.main()
