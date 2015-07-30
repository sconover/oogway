import sys
import os

this_dir = os.path.dirname(os.path.realpath(__file__))
mcpi_relative_path = os.path.join(this_dir, "../../mcpi")
mcgamedata_relative_path = os.path.join(this_dir, "../../mcgamedata")
turtle_path = os.path.join(this_dir, "../")

sys.path.append(mcpi_relative_path)
sys.path.append(mcgamedata_relative_path)
sys.path.append(turtle_path)

import unittest
import mcpi.minecraft
import mcpi
from oogway.turtle import init, chat, begin

class TestTurtle(unittest.TestCase):
  def test_basic(self):
    mcpi_minecraft = mcpi.minecraft.Minecraft.create(name="papadapadapa")
    # mcpi_minecraft.setBlockV2(1, 120, 1, block.STONE.name, variant=block.STONE.VARIANT_ANDESITE.value)
    # mcpi_minecraft.setBlockV2(1, 127, 1, block.STONE.name, block.STONE.VARIANT_ANDESITE)
    # mcpi_minecraft.setBlockV2(1, 130, 1, block.PISTON.name, block.PISTON.FACING_DOWN)

    # mcpi_minecraft.setBlockV2(1, 101, 1, block.DIRT.name)
    # mcpi_minecraft.setBlockV2(1, 102, 1, block.CACTUS.name, block.CACTUS.AGE_15)
    init(mcpi_minecraft, "papadapadapa")
    chat("hi")
    begin()

    # print mcpi_minecraft.player.getTilePos()
    # print mcpi_minecraft.player.getDirection()
    # print mcpi_minecraft.player.getRotation()
    # print mcpi_minecraft.player.getTilePos() + mcpi.vec3.Vec3(10, 0, 0)

# begin()
  # piston appears in front of first player

# begin(x,y,z,0,0)
  # piston appears at x,y,z facing 0,0

# begin("papadapadapa")

# pen_down(blocks.SAND, blocks.SAND.VARIANT_RED_SAND)
# pen_up()
# pen_down() # uses last setting


if __name__ == '__main__':
    unittest.main()
