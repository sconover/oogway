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

  def test_calculate_diffs_angle_68(self):
    # advance in the x-only direction one step, then advance once diagonally (+x and +y). repeat.

    angle = 68

    absolute_x_pos = 100
    absolute_y_pos = 100
    self.assertEqual((1, 0), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 101
    absolute_y_pos = 100
    self.assertEqual((1, 1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 102
    absolute_y_pos = 101
    self.assertEqual((1, 0), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 103
    absolute_y_pos = 101
    self.assertEqual((1, 1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

  def test_calculate_diffs_angle_68(self):
    # advance in the x-only direction one step, then advance once diagonally (+x and -y). repeat.

    angle = 113

    absolute_x_pos = 100
    absolute_y_pos = 100
    self.assertEqual((1, 0), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 101
    absolute_y_pos = 100
    self.assertEqual((1, -1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 102
    absolute_y_pos = 99
    self.assertEqual((1, 0), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 103
    absolute_y_pos = 99
    self.assertEqual((1, -1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

  def test_calculate_diffs_angle_158(self):
    # advance in the negative y-only direction one step, then advance once diagonally (+x and -y). repeat.

    angle = 158

    absolute_x_pos = 100
    absolute_y_pos = 100
    self.assertEqual((0, -1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 100
    absolute_y_pos = 99
    self.assertEqual((1, -1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 101
    absolute_y_pos = 98
    self.assertEqual((0, -1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 101
    absolute_y_pos = 97
    self.assertEqual((1, -1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

  def test_calculate_diffs_angle_203(self):
    # advance in the negative y-only direction one step, then advance once diagonally (-x and -y). repeat.

    angle = 203

    absolute_x_pos = 100
    absolute_y_pos = 100
    self.assertEqual((0, -1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 100
    absolute_y_pos = 99
    self.assertEqual((-1, -1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 99
    absolute_y_pos = 98
    self.assertEqual((0, -1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 99
    absolute_y_pos = 97
    self.assertEqual((-1, -1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

  def test_calculate_diffs_angle_248(self):
    # advance in the negative x-only direction one step, then advance once diagonally (-x and -y). repeat.

    angle = 248

    absolute_x_pos = 100
    absolute_y_pos = 100
    self.assertEqual((-1, 0), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 99
    absolute_y_pos = 100
    self.assertEqual((-1, -1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 98
    absolute_y_pos = 99
    self.assertEqual((-1, 0), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 97
    absolute_y_pos = 99
    self.assertEqual((-1, -1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

  def test_calculate_diffs_angle_293(self):
    # advance in the negative x-only direction one step, then advance once diagonally (-x and +y). repeat.

    angle = 293

    absolute_x_pos = 100
    absolute_y_pos = 100
    self.assertEqual((-1, 0), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 99
    absolute_y_pos = 100
    self.assertEqual((-1, 1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 98
    absolute_y_pos = 101
    self.assertEqual((-1, 0), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 97
    absolute_y_pos = 101
    self.assertEqual((-1, 1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

  def test_calculate_diffs_angle_336(self):
    # advance in the y-only direction one step, then advance once diagonally (-x and +y). repeat.

    angle = 336

    absolute_x_pos = 100
    absolute_y_pos = 100
    self.assertEqual((0, 1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 100
    absolute_y_pos = 101
    self.assertEqual((-1, 1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 99
    absolute_y_pos = 102
    self.assertEqual((0, 1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    absolute_x_pos = 99
    absolute_y_pos = 103
    self.assertEqual((-1, 1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))



if __name__ == '__main__':
    unittest.main()
