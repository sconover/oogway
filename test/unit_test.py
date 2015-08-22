import unittest, os, sys

this_dir = os.path.dirname(os.path.realpath(__file__))
mcgamedata_relative_path = os.path.join(this_dir, "../../mcgamedata")
turtle_path = os.path.join(this_dir, "../")

sys.path.append(mcgamedata_relative_path)
sys.path.append(turtle_path)

from oogway.turtle import init, chat, begin, forward, up, right, left, pen_down, delay, down
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

    self.game = game
    self.connect = connect

    init(self.connect, "papadapadapa")

  def test_chat(self):
    chat("hi")
    chat("there")
    self.assertEqual(["hi", "there"], self.game.chat_log)

  def test_begin_the_begin(self):
    self.game.player.tile_pos = Vector(1,1,1)
    self.game.player.rotation = 2
    begin(start_distance_from_player=5)
    self.assertEqual({(1,1,6):("piston", {"facing":"south"})}, self.game.tiles)

    self.game.reset()
    self.game.player.tile_pos = Vector(1,1,1)
    self.game.player.rotation = 92
    begin(start_distance_from_player=5)
    self.assertEqual({(-4,1,1):("piston", {"facing":"west"})}, self.game.tiles)

    self.game.reset()
    self.game.player.tile_pos = Vector(1,1,1)
    self.game.player.rotation = 182
    begin(start_distance_from_player=5)
    self.assertEqual({(0,1,-4):("piston", {"facing":"north"})}, self.game.tiles)

    self.game.reset()
    self.game.player.tile_pos = Vector(1,1,1)
    self.game.player.rotation = 272
    begin(start_distance_from_player=5)
    self.assertEqual({(6,1,0):("piston", {"facing":"east"})}, self.game.tiles)

  def test_forward(self):
    begin(start_distance_from_player=5, default_trail=[block.GOLD_BLOCK])
    forward()
    forward()
    self.assertEqual({
      (1,1,6):"gold_block",
      (1,1,7):"gold_block",
      (1,1,8):("piston", {"facing":"south"})
    }, self.game.tiles)

if __name__ == '__main__':
    unittest.main()
