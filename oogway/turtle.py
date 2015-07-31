from mcgamedata import block
from collections import namedtuple
from time import sleep

class Position():
  def __init__(self,x,y,z):
    self.x = x
    self.y = y
    self.z = z

class Direction():
  def __init__(self,yaw,pitch,roll):
    self.yaw = yaw
    self.pitch = pitch
    self.roll = roll

class TurtleSession():
  def __init__(self, position, direction):
    self.position = position
    self.direction = direction
    self.delay = 0.1
    self.trail = [block.OBSIDIAN]

class Minecraft():
  def __init__(self):
    self.mcpi_minecraft = None
    self.player = None

  def _m(self):
    return self.mcpi_minecraft

  # TODO: pass prepared functions to a runner and porentially all calls?
  # e.g. turn on stderr debugging with a simple method call... trace()

  def set_block(self, x, y, z, gamedata_block, *gamedata_properties):
    property_to_value = {}
    for p in gamedata_properties:
      p.add_to_dict(property_to_value)
    self._m().setBlockV2(x, y, z, gamedata_block.name, **property_to_value)

  def get_player_rotation_degrees(self):
    return int(self._m().player.getRotation())

  def get_player_tile_pos(self):
    vec = self._m().player.getTilePos()
    return Position(vec.x, vec.y, vec.z)

  def chat(self, message):
    self._m().postToChat(message)

minecraft = Minecraft()

def init(mcpi_minecraft, player=None):
  minecraft.mcpi_minecraft = mcpi_minecraft
  minecraft.player = player
  minecraft.turtle_session = None

def chat(message):
  minecraft.chat(message)

def begin():
  pos = minecraft.get_player_tile_pos()
  rotation_degrees = minecraft.get_player_rotation_degrees()

  # TODO: trig.
  # dirty for now.

  x_diff = 0
  y_diff = 0
  z_diff = 0
  facing = None
  yaw = None
  if rotation_degrees >= 315 and rotation_degrees < 360 or \
     rotation_degrees >= 0 and rotation_degrees < 45:
    z_diff = 10 # south
    facing = block.PISTON.FACING_SOUTH
    yaw = 0
  elif rotation_degrees >= 45 and rotation_degrees < 135:
    x_diff = -10
    facing = block.PISTON.FACING_WEST
    yaw = 90
  elif rotation_degrees >= 135 and rotation_degrees < 225:
    z_diff = -10 # north
    facing = block.PISTON.FACING_NORTH
    yaw = 180
  else:
    x_diff = 10
    facing = block.PISTON.FACING_EAST
    yaw = 270

  start_x = pos.x + x_diff
  start_y = pos.y + y_diff
  start_z = pos.z + z_diff
  minecraft.turtle_session = TurtleSession(Position(start_x, start_y, start_z), Direction(yaw, 90, 0))
  _draw_turtle()

def _draw_turtle():
  turtle = minecraft.turtle_session
  minecraft.set_block(
    turtle.position.x, turtle.position.y, turtle.position.z,
    block.PISTON, _turtle_facing())

def _turtle_facing():
  turtle = minecraft.turtle_session
  if turtle.direction.yaw == 0:
    return block.PISTON.FACING_SOUTH
  elif turtle.direction.yaw == 90:
    return block.PISTON.FACING_WEST
  elif turtle.direction.yaw == 180:
    return block.PISTON.FACING_NORTH
  else:
    return block.PISTON.FACING_EAST

def _draw_block(position, *block_args):
  minecraft.set_block(
    position.x, position.y, position.z,
    *block_args)

def _move(x,y,z):
  turtle = minecraft.turtle_session
  sleep(turtle.delay)
  a = turtle.position
  b = Position(x,y,z)

  turtle.position = b
  _draw_turtle()
  _draw_block(a, *turtle.trail)


def _move_relative(x_diff, y_diff, z_diff):
  turtle = minecraft.turtle_session
  _move(
      turtle.position.x + x_diff,
      turtle.position.y + y_diff,
      turtle.position.z + z_diff)

def forward():
  turtle = minecraft.turtle_session
  x_diff = 0
  y_diff = 0
  z_diff = 0

  if turtle.direction.pitch == 0:
    y_diff = 1
  elif turtle.direction.pitch == 180:
    y_diff = -1
  elif turtle.direction.yaw == 0:
    z_diff = 1
  elif turtle.direction.yaw == 90:
    x_diff = -1
  elif turtle.direction.yaw == 180:
    z_diff = -1
  else:
    x_diff = 1

  _move_relative(x_diff, y_diff, z_diff)

def pen_down(*block_args):
  turtle = minecraft.turtle_session
  turtle.trail = block_args

# check(is(block.AIR))
# check(is_not(block.AIR))
#   is_not(block.AIR) ... predicate defs return curried functions
# both, neither, either
# ...good way to teach predicate logic

def right(degrees):
  turtle = minecraft.turtle_session
  if (abs(degrees) not in [0, 90, 180, 270]):
      raise Exception("sorry, only 0, 90, 180, and 270 are allowed for now.")

  turtle.direction.yaw += degrees
  if turtle.direction.yaw >= 360:
      turtle.direction.yaw = turtle.direction.yaw - 360
  elif turtle.direction.yaw < 0:
      turtle.direction.yaw = turtle.direction.yaw + 360
  _draw_turtle()

def left(degrees):
  right(-1 * degrees)

def up(degrees):
  turtle = minecraft.turtle_session
  if (abs(degrees) not in [0, 90, 180, 270]):
      raise Exception("sorry, only 0, 90, 180, and 270 are allowed for now.")

  turtle.direction.pitch -= degrees
  if turtle.direction.pitch >= 360:
      turtle.direction.pitch = turtle.direction.pitch - 360
  elif turtle.direction.pitch < 0:
      turtle.direction.pitch = turtle.direction.pitch + 360
  _draw_turtle()

def down(degrees):
  up(-1 * degrees)
