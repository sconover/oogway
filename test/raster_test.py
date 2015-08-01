import sys
import os

this_dir = os.path.dirname(os.path.realpath(__file__))
turtle_path = os.path.join(this_dir, "../")

sys.path.append(turtle_path)

import unittest
from oogway.raster import calculate_increment_2d


class TestRaster(unittest.TestCase):
  def test_calculate_diffs_angle_23(self):
    # advance in the y-only direction one step, then advance once diagonally (+x and +y). repeat.

    angle = 23

    absolute_x_pos = 100
    absolute_y_pos = 100
    self.assertEqual((0, 1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 100
    absolute_y_pos = 101
    self.assertEqual((1, 1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 101
    absolute_y_pos = 102
    self.assertEqual((0, 1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 101
    absolute_y_pos = 103
    self.assertEqual((1, 1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

  def test_calculate_diffs_angle_45(self):
    # advance diagonally (+x and +y). repeat.

    angle = 45

    absolute_x_pos = 100
    absolute_y_pos = 100
    self.assertEqual((1, 1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 101
    absolute_y_pos = 101
    self.assertEqual((1, 1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

  def test_calculate_diffs_angle_12(self):
    # advance in the y-only direction three steps, then advance once diagonally (+x and +y). repeat.

    angle = 12

    absolute_x_pos = 100
    absolute_y_pos = 100
    self.assertEqual((0, 1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 100
    absolute_y_pos = 101
    self.assertEqual((0, 1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 100
    absolute_y_pos = 102
    self.assertEqual((0, 1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 100
    absolute_y_pos = 103
    self.assertEqual((1, 1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 101
    absolute_y_pos = 104
    self.assertEqual((0, 1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))


if __name__ == '__main__':
    unittest.main()
