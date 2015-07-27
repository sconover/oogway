import sys
import os

this_dir = os.path.dirname(os.path.realpath(__file__))
mcpi_relative_path = os.path.join(this_dir, "../../mcpi")
turtle_path = os.path.join(this_dir, "../turtle")

sys.path.append(mcpi_relative_path)
sys.path.append(turtle_path)

import unittest
import mcpi.minecraft
import turtle

class TestTurtle(unittest.TestCase):
  def test_basic(self):
    mcpi_minecraft = mcpi.minecraft.Minecraft.create()
    mcpi_minecraft.setBlock(1, 110, 1, mcpi.block.GOLD_BLOCK.id)

if __name__ == '__main__':
    unittest.main()
