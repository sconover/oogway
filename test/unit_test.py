import unittest, os, sys

this_dir = os.path.dirname(os.path.realpath(__file__))
mcgamedata_relative_path = os.path.join(this_dir, "../../mcgamedata")
turtle_path = os.path.join(this_dir, "../")

sys.path.append(mcgamedata_relative_path)
sys.path.append(turtle_path)

from oogway.turtle import init, chat, begin, forward, up, right, left, pen_down, pen_up, delay, down
from mcgamedata import block

class Vector():
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

class FakeMcpiPlayer():
  def __init__(self, rotation, tile_pos):
    self.rotation = rotation
    self.tile_pos = tile_pos

  def getRotation(self):
    return self.rotation

  def getTilePos(self):
    return self.tile_pos

class FakeMcpi():
  def __init__(self, player):
    self.player = player
    self.reset()

  def reset(self):
    self.chat_log = []
    self.tiles = {}

  def setBlockV2(self, x, y, z, block_type_name, **property_to_value):
    if property_to_value == {}:
      self.tiles[(x,y,z)] = block_type_name
    else:
      self.tiles[(x,y,z)] = (block_type_name, property_to_value)

  def postToChat(self, message):
    self.chat_log.append(message)

  def get_tile(self, x, y, z):
    print self.tiles
    return self.tiles[(x,y,z)]

class TestUnit(unittest.TestCase):
  def setUp(self):
    game = FakeMcpi(FakeMcpiPlayer(3, Vector(1,1,1)))

    def connect():
      return game

    slept = []
    def fake_sleep(interval):
      slept.append(interval)

    self.game = game
    self.connect = connect
    self.slept = slept

    init(self.connect, "papadapadapa")

    def begin_for_testing():
      begin(start_distance_from_player=5, default_trail=[block.GOLD_BLOCK], sleep_function=fake_sleep)

    self.begin_for_testing = begin_for_testing

  def test_chat(self):
    chat("hi")
    chat("there")
    self.assertEqual(["hi", "there"], self.game.chat_log)

  def test_begin_the_begin(self):
    self.game.player.tile_pos = Vector(1,1,1)
    self.game.player.rotation = 2
    self.begin_for_testing()
    self.assertEqual({(1,1,6):("piston", {"facing":"south"})}, self.game.tiles)

    self.game.reset()
    self.game.player.tile_pos = Vector(1,1,1)
    self.game.player.rotation = 92
    self.begin_for_testing()
    self.assertEqual({(-4,1,1):("piston", {"facing":"west"})}, self.game.tiles)

    self.game.reset()
    self.game.player.tile_pos = Vector(1,1,1)
    self.game.player.rotation = 182
    self.begin_for_testing()
    self.assertEqual({(0,1,-4):("piston", {"facing":"north"})}, self.game.tiles)

    self.game.reset()
    self.game.player.tile_pos = Vector(1,1,1)
    self.game.player.rotation = 272
    self.begin_for_testing()
    self.assertEqual({(6,1,0):("piston", {"facing":"east"})}, self.game.tiles)

  def test_forward(self):
    self.begin_for_testing()
    forward()
    forward()

    self.assertEqual({
      (1,1,6): "gold_block",
      (1,1,7): "gold_block",
      (1,1,8): ("piston", {"facing":"south"})
    }, self.game.tiles)

  def test_pen_down_pen_up(self):
    self.begin_for_testing()
    forward()
    forward()
    pen_up()
    forward()
    forward()
    pen_down(block.GOLD_BLOCK)
    forward()
    forward()

    self.assertEqual({
      (1,1,6):  "gold_block",
      (1,1,7):  "gold_block",
      (1,1,8):  "air",
      (1,1,9):  "air",
      (1,1,10): "gold_block",
      (1,1,11): "gold_block",
      (1,1,12): ("piston", {"facing":"south"})
    }, self.game.tiles)

  def test_show_that_pen_up_is_currently_destructive(self):
    self.begin_for_testing()
    forward()
    forward()
    forward()

    self.begin_for_testing()
    pen_up()
    forward()

    self.assertEqual({
      (1,1,6): "air",
      (1,1,7): ("piston", {"facing":"south"}), # the second turtle, overwriting the first path
      (1,1,8): "gold_block",
      (1,1,9): ("piston", {"facing":"south"}) # the original turtle
    }, self.game.tiles)

if __name__ == '__main__':
    unittest.main()
