from mcgamedata import block
from collections import namedtuple

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
    self.trail = mcpi.block.OBSIDIAN

class Minecraft():
  def __init__(self):
    self.mcpi_minecraft = None
    self.player = None
    self.turtle_session = None

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
  if rotation_degrees >= 315 and rotation_degrees < 360 or \
     rotation_degrees >= 0 and rotation_degrees < 45:
    z_diff = 10 # south
    facing = block.PISTON.FACING_SOUTH
  elif rotation_degrees >= 45 and rotation_degrees < 135:
    x_diff = -10
    facing = block.PISTON.FACING_WEST
  elif rotation_degrees >= 135 and rotation_degrees < 225:
    z_diff = -10 # north
    facing = block.PISTON.FACING_NORTH
  else:
    x_diff = 10
    facing = block.PISTON.FACING_EAST

  minecraft.set_block(
    pos.x + x_diff,
    pos.y + y_diff,
    pos.z + z_diff,
    block.PISTON, facing)


# turtle = None

# def begin(x=None, y=None, z=None, yaw_angle=None, pitch_angle=None):
#   if x == None:
    # use current player (facing away)
    # fall back to facing away from first player
    # fall back to 1, 100, 1

  # turtle = TurtleSession()
  # ...piston appears in front of player...facing the other direction...

# TODO: this is replaced by pendown
# def trail(block_type,*args,**kwargs):
#   # TODO: check type
#   turtle.trail = block_type

# def _move(x,y,z):
#   sleep(turtle.delay)
#   a = turtle.position
#   b = Position(x,y,z)

#   # imagine a transaction...
#   minecraft.change_block_type(b.x,b.y,b.z,mcpi.block.GOLD_BLOCK)
#   turtle.position = b

#   minecraft.change_block_type(b.x,b.y,b.z,turtle.trail)


# def move_relative(x_diff, y_diff, z_diff):
#   _move(
#       turtle.pos.x + x_diff,
#       turtle.pos.y + y_diff,
#       turtle.pos.z + z_diff)

# def forward():
#   x_diff = 0
#   y_diff = 0
#   z_diff = 0
#   if turtle.direction.yaw == 0:
#       x_diff = 1
#   elif turtle.direction.yaw == 90:
#       z_diff = 1
#   elif turtle.direction.yaw == 180:
#       x_diff = -1
#   else:
#       z_diff = -1

#   if turtle.direction.pitch == 0:
#       y_diff = 1
#   elif turtle.direction.pitch == 180:
#       y_diff = -1

#   move_relative(x_diff, y_diff, z_diff)

# def right(degrees):
#   if (abs(degrees) not in [0, 90, 180, 270]):
#       raise Exception("sorry, only 0, 90, 180, and 270 are allowed for now.")

#   turtle.direction.yaw += degrees
#   if turtle.direction.yaw >= 360:
#       turtle.direction.yaw = turtle.direction.yaw - 360
#   elif turtle.direction.yaw < 0:
#       turtle.direction.yaw = turtle.direction.yaw + 360


# def left(degrees):
#   right(-1 * degrees)

# def up(degrees):
#   if (abs(degrees) not in [0, 90, 180, 270]):
#       raise Exception("sorry, only 0, 90, 180, and 270 are allowed for now.")

#   turtle.direction.pitch -= degrees
#   if turtle.direction.pitch >= 360:
#       turtle.direction.pitch = turtle.direction.pitch - 360
#   elif turtle.direction.pitch < 0:
#       turtle.direction.pitch = turtle.direction.pitch + 360

# def down(degrees):
#   up(-1 * degrees)
