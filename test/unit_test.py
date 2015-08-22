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
    self.chat_log = []

  def setBlockV2(self, x, y, z, block_type_name, property_to_value):
    pass

  def postToChat(self, message):
    self.chat_log.append(message)

class TestUnit(unittest.TestCase):
  def setUp(self):
    game = FakeMcpi(FakeMcpiPlayer(90, Vector(1,1,1)))

    def connect():
      return game

    self.game = game
    self.connect = connect

    init(self.connect, "papadapadapa")

  def test_chat(self):
    chat("hi")
    chat("there")
    self.assertEqual(["hi", "there"], self.game.chat_log)

if __name__ == '__main__':
    unittest.main()
