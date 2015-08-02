import sys
import os

this_dir = os.path.dirname(os.path.realpath(__file__))
turtle_path = os.path.join(this_dir, "../")

sys.path.append(turtle_path)

import unittest
from oogway.vector import add, subtract, equal
# from oogway.orientation import Position, Direction

class TestVector(unittest.TestCase):
    def test_add(self):
        u = [1, 2]
        v = [3, 4]
        self.assertEqual([4, 6], add(u, v))

    def test_subtract(self):
        u = [1, 2]
        v = [3, 4]
        self.assertEqual([-2, -2], subtract(u, v))

    def test_equal(self):
        u = [1, 2]
        v = [3, 4]
        self.assertEqual(False, equal(u, v))

        u = [1, 2]
        v = [1, 2]
        self.assertEqual(True, equal(u, v))

if __name__ == '__main__':
    unittest.main()

