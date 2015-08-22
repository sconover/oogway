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
from oogway.turtle import init, chat, begin, forward, up, right, left, pen_down, delay, down
from mcgamedata import block


class TestIntegration(unittest.TestCase):
  def test_basic(self):
    def connect():
        # connect to minecraft server running on localhost, 25565 (default port)
        return mcpi.minecraft.Minecraft.create()

    # mcpi_minecraft.setBlockV2(1, 120, 1, block.STONE.name, variant=block.STONE.VARIANT_ANDESITE.value)
    # mcpi_minecraft.setBlockV2(1, 127, 1, block.STONE.name, block.STONE.VARIANT_ANDESITE)
    # mcpi_minecraft.setBlockV2(1, 130, 1, block.PISTON.name, block.PISTON.FACING_DOWN)

    # mcpi_minecraft.setBlockV2(1, 101, 1, block.DIRT.name)
    # mcpi_minecraft.setBlockV2(1, 102, 1, block.CACTUS.name, block.CACTUS.AGE_15)
    init(connect, "papadapadapa")
    chat("hi")
    # begin()
    # pen_down(block.GOLD_BLOCK)

    # forward()
    # forward()
    # forward()
    # forward()

    # up(90)
    # forward()
    # forward()
    # forward()
    # forward()

    # down(90)
    # right(90)
    # forward()
    # forward()
    # forward()
    # forward()

    begin()
    pen_down(block.GOLD_BLOCK)

    # forward()
    # forward()

    # right(90)
    # forward()
    # forward()

    # up(90)
    # forward()
    # forward()



    forward()
    forward()

    up(90)
    forward()
    forward()

    right(90) # turtle does not actually turn, keeps going up
    forward()
    forward()


    # forward()
    # forward()

    # up(90)
    # forward()
    # forward()

    # down(90) # cancels out the up
    # right(90) # turtle turns right
    # forward()
    # forward()


    # start_task(living.OCELOT.SIT)
    # reset_task(living.OCELOT.SIT)

    # up(45)
    # forward()
    # forward()
    # forward()
    # forward()
    # down(90)
    # forward()
    # forward()
    # forward()
    # forward()

    # up(90)
    # forward()
    # forward()
    # forward()
    # forward()

    # right(90)
    # forward()
    # forward()
    # forward()
    # forward()

    # left(90)
    # forward()
    # forward()
    # forward()
    # forward()

    # down(90)
    # forward()
    # forward()
    # forward()
    # forward()

    # left(45)
    # forward()
    # forward()
    # forward()
    # forward()

    # right(90)
    # forward()
    # forward()
    # forward()
    # forward()
    # for i in xrange(10):
    #     forward()

    # right(90)
    # for i in xrange(10):
    #     forward()

    # up(30)
    # delay(0)

    # def poly(sides, side_length):
    #     degrees = 360/sides
    #     for i in xrange(sides):
    #         right(degrees)
    #         for j in xrange(side_length):
    #             forward()
    # # # # delay(0.1)
    # # delay(0)

    # # down(30)

    # def cylinder(height):
    #     for i in xrange(height):
    #         poly(30, 3)
    #         up(90)
    #         forward()
    #         down(90)

    # # cylinder(40)

    # def square(side):
    #     for i in range(0, side, -1):
    #         poly(4, i)
    #         left(90)
    #         forward()
    #         right(90)

    # # square(8)
    # def square(side):
    #     for i in range(side, 1, -1):
    #         poly(4, i)
    #         right(90)
    #         forward()
    #         right(90)
    #         forward()
    #         left(180)



    # def cube(side):
    #     for i in xrange(side):
    #         square(side)
    #         up(90)
    #         forward()
    #         down(90)
    #         right(90)
    #         forward()
    #         right(90)
    #         forward()
    #         left(90)

    # cube(5)
    # for i in xrange(8):
    #     if i % 2 == 0:
    #         up(60)
    #     else:
    #         down(60)
    #     poly(8, 5)
    #     poly(8, 5)
    #     poly(8, 5)
    #     right(45)

    # repeat = 12
    # for i in xrange(repeat):
    #     poly(6, 10)
    #     down(360/repeat)


    # step_size = 5
    # for i in xrange(360/step_size):
    #     up(step_size)
    #     forward()
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
