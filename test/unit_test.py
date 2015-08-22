import unittest, os, sys

this_dir = os.path.dirname(os.path.realpath(__file__))
mcgamedata_relative_path = os.path.join(this_dir, "../../mcgamedata")
turtle_path = os.path.join(this_dir, "../")

sys.path.append(mcgamedata_relative_path)
sys.path.append(turtle_path)

from oogway.turtle import init, chat, begin, forward, up, right, left, pen_down, delay, down
from mcgamedata import block

class Vector():
  def __init__(self):
    self.x = 1
    self.y = 1
    self.z = 1

class FakeMcpiPlayer():
  def __init__(self):
    self.tile_pos = Vector()
    self.rotation = 90

  def getRotation(self):
    return self.rotation

  def getTilePos(self):
    return self.tile_pos

class FakeMcpi():
  def __init__(self):
    self.player = FakeMcpiPlayer()
    self.chat_log = []

  def setBlockV2(self, x, y, z, block_type_name, property_to_value):
    pass

  def postToChat(self, message):
    self.chat_log.append(message)

class TestUnit(unittest.TestCase):
  def setUp(self):
    game = FakeMcpi()

    def connect():
      return game

    self.game = game
    self.connect = connect

  def test_chat(self):

    init(self.connect, "papadapadapa")
    chat("hi")
    chat("there")

    self.assertEqual(["hi", "there"], self.game.chat_log)

if __name__ == '__main__':
    unittest.main()
