import unittest, doctest, os, sys, re
import logging
import sys

this_dir = os.path.dirname(os.path.realpath(__file__))
mcgamedata_relative_path = os.path.join(this_dir, "../../mcgamedata")
turtle_path = os.path.join(this_dir, "../")

sys.path.append(mcgamedata_relative_path)
sys.path.append(turtle_path)

from oogway.sphere_math import calculate_point_on_sphere2
from oogway.orientation import Direction, Position

NORTH_HORIZON = Direction(180,0,0)
EAST_HORIZON = Direction(-90,0,0)
SOUTH_HORIZON = Direction(0,0,0)
WEST_HORIZON = Direction(90,0,0)

STRAIGHT_UP = Direction(0,-90,0)
STRAIGHT_DOWN = Direction(0,90,0)

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler(stream=sys.stderr)
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('oogway.sphere_math').addHandler(console)

class TestUnit(unittest.TestCase):
    def test_basics(self):
        self.assertEqual(Position(0, 0, -1), calculate_point_on_sphere2(NORTH_HORIZON, 1))
        self.assertEqual(Position(1, 0, 0), calculate_point_on_sphere2(EAST_HORIZON, 1))
        self.assertEqual(Position(0, 0, 1), calculate_point_on_sphere2(SOUTH_HORIZON, 1))
        self.assertEqual(Position(-1, 0, 0), calculate_point_on_sphere2(WEST_HORIZON, 1))

        # alternative north
        self.assertEqual(Position(0, 0, 1), calculate_point_on_sphere2(Direction(-180,0,0), 1))

        self.assertEqual(Position(0, 1, 0), calculate_point_on_sphere2(STRAIGHT_UP, 1))
        self.assertEqual(Position(0, -1, 0), calculate_point_on_sphere2(STRAIGHT_DOWN, 1))

    def test_angles(self):
        self.assertEqual(Position(0, 0.707, 0.707), calculate_point_on_sphere2(Direction(0,-45,0), 1))

if __name__ == '__main__':
    unittest.main()