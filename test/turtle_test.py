import sys
import os

this_dir = os.path.dirname(os.path.realpath(__file__))
mcpi_relative_path = os.path.join(this_dir, "../../mcpi")
turtle_path = os.path.join(this_dir, "../turtle")

sys.path.append(mcpi_relative_path)
sys.path.append(turtle_path)

import unittest
import mcpi.minecraft
from mcpi.gamedata import block
import turtle

class TestTurtle(unittest.TestCase):
  def test_basic(self):
    mcpi_minecraft = mcpi.minecraft.Minecraft.create()
    mcpi_minecraft.setBlockV2(1, 120, 1, block.STONE.name, variant=block.STONE.VARIANT_ANDESITE.value)

# pen_down(blocks.SAND, blocks.SAND.VARIANT_RED_SAND)
# pen_up()

if __name__ == '__main__':
    unittest.main()
