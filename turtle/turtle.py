import mcpi

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
    self.mcpi_minecraft_connection = None
    self.player_name = None
    self.turtle_session = None

  def _m(self):
    return self.mcpi_minecraft_connection

  def change_block_type(self, x, y, z, block_type):
    _m().setBlock(x, y, z, block_type.id)

minecraft = Minecraft()

def init(mcpi_minecraft_connection, player_name):
  minecraft.mcpi_minecraft_connection = mcpi_minecraft_connection
  minecraft.player_name = player_name

turtle = None

def begin():
  turtle = TurtleSession()
  # ...piston appears in front of player...

def block_type(block_type):
  # TODO: check type
  turtle.trail = block_type

def _move(x,y,z):
  sleep(turtle.delay)
  a = turtle.position
  b = Position(x,y,z)

  # imagine a transaction...
  minecraft.change_block_type(b.x,b.y,b.z,mcpi.block.GOLD_BLOCK)
  turtle.position = b

  minecraft.change_block_type(b.x,b.y,b.z,turtle.trail)


def move_relative(x_diff, y_diff, z_diff):
  _move(
      turtle.pos.x + x_diff,
      turtle.pos.y + y_diff,
      turtle.pos.z + z_diff)

def forward():
  x_diff = 0
  y_diff = 0
  z_diff = 0
  if turtle.direction.yaw == 0:
      x_diff = 1
  elif turtle.direction.yaw == 90:
      z_diff = 1
  elif turtle.direction.yaw == 180:
      x_diff = -1
  else:
      z_diff = -1

  if turtle.direction.pitch == 0:
      y_diff = 1
  elif turtle.direction.pitch == 180:
      y_diff = -1

  move_relative(x_diff, y_diff, z_diff)

def right(degrees):
  if (abs(degrees) not in [0, 90, 180, 270]):
      raise Exception("sorry, only 0, 90, 180, and 270 are allowed for now.")

  turtle.direction.yaw += degrees
  if turtle.direction.yaw >= 360:
      turtle.direction.yaw = turtle.direction.yaw - 360
  elif turtle.direction.yaw < 0:
      turtle.direction.yaw = turtle.direction.yaw + 360


def left(degrees):
  right(-1 * degrees)

def up(degrees):
  if (abs(degrees) not in [0, 90, 180, 270]):
      raise Exception("sorry, only 0, 90, 180, and 270 are allowed for now.")

  turtle.direction.pitch -= degrees
  if turtle.direction.pitch >= 360:
      turtle.direction.pitch = turtle.direction.pitch - 360
  elif turtle.direction.pitch < 0:
      turtle.direction.pitch = turtle.direction.pitch + 360

def down(degrees):
  up(-1 * degrees)
