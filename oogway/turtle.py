from mcgamedata import block, block_definition, living, living_definition
from collections import namedtuple
from time import sleep
from sphere_math import calculate_point_on_sphere
from orientation import Position, Direction

class TurtleSession():
  def __init__(self, position, direction, default_trail, sleep_function):
    self.position = position
    self.direction = direction
    self.delay = 0.1
    self.trail = default_trail
    self.sleep = sleep_function
    self.living_things_selected = {}

class Minecraft():
  def __init__(self):
    self.mcpi_minecraft_connect_function = None
    self.player_name = None
    self._mcpi_minecraft = None

  def _m(self):
    if self._mcpi_minecraft == None:
      self._mcpi_minecraft = self.mcpi_minecraft_connect_function()
      self._mcpi_minecraft.player.name = self.player_name
    return self._mcpi_minecraft

  def reconnect(self):
    self._mcpi_minecraft = None
    self._m()

  def is_connected(self):
    return self._mcpi_minecraft != None

  # TODO: pass prepared functions to a runner and potentially all calls?
  # e.g. turn on stderr debugging with a simple method call... trace()

  def batch(self, f):
    self._m().startBatch()
    f(self)
    self._m().endBatch() # todo: guard against failed ends from exceptions/errors?

  def set_block(self, x, y, z, gamedata_block, *gamedata_properties):
    property_to_value = {}
    for p in gamedata_properties:
      p.add_to_dict(property_to_value)
    # cast to int. we're mapping a continuous space of very high precision,
    # on to a grid.
    self._m().setBlockV2(int(x), int(y), int(z), gamedata_block.name, **property_to_value)

  def spawn_entity(self, x, y, z, gamedata_entity, *entity_properties):
    property_to_value = {}
    for p in entity_properties:
      p.add_to_dict(property_to_value)

    if "owner" not in property_to_value and self.player_name != None:
      property_to_value["owner"] = self.player_name

    return self._m().entity.spawnV2(int(x), int(y), int(z), gamedata_entity.name, **property_to_value)

  def living_entity_start_task(self, entity_uuid, task):
    self._m().entity.startTaskV2(entity_uuid, task.task_name)

  def living_entity_reset_task(self, entity_uuid, task):
    self._m().entity.resetTaskV2(entity_uuid, task.task_name)

  def get_all_entities_in_bounding_box(self, cube_corner_1, cube_corner_2):
    return self._m().entity.getAllInBoundingCube(
      cube_corner_1.x, cube_corner_1.y, cube_corner_1.z,
      cube_corner_2.x, cube_corner_2.y, cube_corner_2.z)

  def get_player_rotation_degrees(self):
    return int(self._m().player.getRotation())

  def get_player_tile_pos(self):
    vec = self._m().player.getTilePos()
    return Position(vec.x, vec.y, vec.z)

  def chat(self, message):
    self._m().postToChat(message)

minecraft = Minecraft()

name_to_block = {}
for block_type in block.ALL:
  name_to_block[block_type.name] = block_type

name_to_living = {}
for living_type in living.ALL:
  name_to_living[living_type.name] = living_type

def init(mcpi_minecraft_connect_function, player=None):
  minecraft.mcpi_minecraft_connect_function = mcpi_minecraft_connect_function
  if player:
    minecraft.player_name = player
  if minecraft.is_connected():
    minecraft.reconnect()

  minecraft.turtle_session = None

def chat(message):
  minecraft.chat(message)

def begin(start_distance_from_player=5, default_trail=[block.GOLD_BLOCK], sleep_function=sleep):
  pos = minecraft.get_player_tile_pos()
  rotation_degrees = minecraft.get_player_rotation_degrees()
  if rotation_degrees < 0:
    rotation_degrees = 360 + rotation_degrees

  horizon_pitch = 90

  facing = _facing_based_on_yaw(rotation_degrees)
  yaw = 0
  if facing == block.PISTON.FACING_SOUTH:
    yaw = 180
  if facing == block.PISTON.FACING_WEST:
    yaw = 270
  elif facing == block.PISTON.FACING_NORTH:
    yaw = 0
  elif facing == block.PISTON.FACING_EAST:
    yaw = 90
  position_diff = calculate_point_on_sphere(direction=Direction(yaw, horizon_pitch, 0), radius=start_distance_from_player)

  start_x = pos.x + position_diff.x
  start_y = pos.y + position_diff.y
  start_z = pos.z + position_diff.z
  minecraft.turtle_session = TurtleSession(
    Position(start_x, start_y, start_z),
    Direction(yaw, horizon_pitch, 0),
    default_trail,
    sleep_function)
  _draw_turtle()

def _draw_turtle():
  turtle = minecraft.turtle_session
  minecraft.set_block(
    turtle.position.x, turtle.position.y, turtle.position.z,
    block.PISTON, _turtle_facing())

def _facing_based_on_yaw(yaw):
  turtle = minecraft.turtle_session

  facing = None
  if yaw >= 0:
    facing = block.PISTON.FACING_WEST
  if yaw >= 45:
    facing = block.PISTON.FACING_NORTH
  if yaw >= 135:
    facing = block.PISTON.FACING_EAST
  if yaw >= 225:
    facing = block.PISTON.FACING_SOUTH
  if yaw >= 315:
    facing = block.PISTON.FACING_WEST

  return facing

def _opposite_facing(facing):
  if facing == block.PISTON.FACING_SOUTH:
    return block.PISTON.FACING_NORTH
  if facing == block.PISTON.FACING_NORTH:
    return block.PISTON.FACING_SOUTH

  if facing == block.PISTON.FACING_EAST:
    return block.PISTON.FACING_WEST
  if facing == block.PISTON.FACING_WEST:
    return block.PISTON.FACING_EAST

  if facing == block.PISTON.FACING_DOWN:
    return block.PISTON.FACING_UP
  if facing == block.PISTON.FACING_UP:
    return block.PISTON.FACING_DOWN

def _turtle_facing():
  turtle = minecraft.turtle_session

  facing_from_yaw = _facing_based_on_yaw(turtle.direction.yaw)
  facing = facing_from_yaw

  if turtle.direction.pitch >= 0:
    facing = facing = block.PISTON.FACING_UP
  if turtle.direction.pitch >= 45:
    facing = facing_from_yaw
  if turtle.direction.pitch >= 135:
    facing = block.PISTON.FACING_DOWN
  if turtle.direction.pitch >= 225:
    facing = _opposite_facing(facing_from_yaw)
  if turtle.direction.pitch >= 315:
    facing = block.PISTON.FACING_UP

  return facing

def _draw_thing(position, *args):
  turtle = minecraft.turtle_session

  if isinstance(args[0], block_definition.BlockDefinition):
    minecraft.set_block(
      position.x, position.y, position.z,
      *args)
  elif isinstance(args[0], living_definition.LivingDefinition):
    entity = minecraft.spawn_entity(
      position.x, position.y, position.z,
      args[0])
    _select_entity(entity)
    _draw_thing(position, block.AIR)
  else:
    raise Exception("don't know what to do with " + str(args))

def _select_entity(entity):
  turtle = minecraft.turtle_session
  if entity.type in name_to_living:
    turtle.living_things_selected[entity.uuid] = name_to_living[entity.type]
  else:
    turtle.living_things_selected[entity.uuid] = None

def _move(x,y,z):
  turtle = minecraft.turtle_session
  turtle.sleep(turtle.delay)
  a = turtle.position
  b = Position(x,y,z)

  turtle.position = b
  _draw_thing(a, *turtle.trail)
  _draw_turtle()

def _move_relative(x_diff, y_diff, z_diff):
  turtle = minecraft.turtle_session
  _move(
      turtle.position.x + x_diff,
      turtle.position.y + y_diff,
      turtle.position.z + z_diff)

def delay(seconds):
  minecraft.turtle_session.delay = seconds

def forward():
  turtle = minecraft.turtle_session
  # print turtle.direction
  position_diff = calculate_point_on_sphere(direction=turtle.direction, radius=1)
  # print position_diff
  _move_relative(position_diff.x, position_diff.y, position_diff.z)

def pen_down(*args):
  turtle = minecraft.turtle_session
  turtle.trail = args

# TODO: we really need to replace the turtle with the block that was there (exactly as it was)
# this is an invitation to create a remote call that sends down all of the block info at the
# given position, such that we can remember it.
#
# ...also leads into creating a "test" method - to test the block just in front of us
#
# for network efficiency, perhaps the remote calls should return detail for all blocks adjacent to
# the current block? (though, that could be a lot of data)...
#
# ...or make "return the block in x direction" or "at x coords" an optional param...
#
# *** ...or just make a batch endpoint ***
def pen_up(*args):
  turtle = minecraft.turtle_session
  turtle.trail = [block.AIR] # this is destructive.

def living_things():
  turtle = minecraft.turtle_session
  return turtle.living_things_selected

def _select_all_living_of_type(task, entities):
  return filter(lambda entity_uuid: entities[entity_uuid] == name_to_living[task.entity_name], entities)

def start_task(task, selector=_select_all_living_of_type):
  def all_tasks_at_once(mc):
    for entity_uuid in _select_all_living_of_type(task, living_things()):
      mc.living_entity_start_task(entity_uuid, task)
  minecraft.batch(all_tasks_at_once)

def reset_task(task, selector=_select_all_living_of_type):
  def all_tasks_at_once(mc):
    for entity_uuid in _select_all_living_of_type(task, living_things()):
      mc.living_entity_reset_task(entity_uuid, task)
  minecraft.batch(all_tasks_at_once)

def current_position():
  return minecraft.get_player_tile_pos()

HORIZON_DISTANCE = 32*16 # 32 chunks * 16 blocks / chunk

def cube_centered_on(position, center_to_edge_length=HORIZON_DISTANCE):
  x1 = position.x - center_to_edge_length
  y1 = max(1, position.y - center_to_edge_length)
  z1 = position.z - center_to_edge_length

  x2 = position.x + center_to_edge_length
  y2 = min(254, position.y + center_to_edge_length)
  z2 = position.z + center_to_edge_length

  return (Position(x1, y1, z1), Position(x2, y2, z2))

def nearby():
  return cube_centered_on(current_position(), center_to_edge_length=HORIZON_DISTANCE)

def select_living_things(cube_corners):
  results = minecraft.get_all_entities_in_bounding_box(cube_corners[0], cube_corners[1])
  for entity in results:
    _select_entity(entity)

# select_living_things(cube_from_point(current_position(), HORIZON_DISTANCE)))

# path of blocks
#  what if it's sand and the sand falls?

# pen_down(living.OCELOT)

# living_things()
  # path of uuids...

# start_task(living.ANY.FOLLOW_OWNER) # implicit select of things that have this task
# start_task(living.OCELOT.FOLLOW_OWNER) # implicit select of ocelots
# start_task(living.OCELOT.FOLLOW_OWNER, select=recent(living.OCELOT))
# start_task(living.OCELOT.FOLLOW_OWNER, select=recent(living.OCELOT, offset))
# start_task(living.OCELOT.FOLLOW_OWNER, select=recent(living.OCELOT, range))
# start_task(living.OCELOT.FOLLOW_OWNER, select=beginning(living.OCELOT, offset))
# start_task(living.OCELOT.FOLLOW_OWNER, select=beginning(living.OCELOT, range))

# what if some no longer exist? best effort?


# check(is(block.AIR))
# check(is_not(block.AIR))
#   is_not(block.AIR) ... predicate defs return curried functions
# both, neither, either
# ...good way to teach predicate logic

def right(degrees):
  turtle = minecraft.turtle_session

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

  turtle.direction.pitch -= degrees
  if turtle.direction.pitch >= 360:
      turtle.direction.pitch -= 360
  elif turtle.direction.pitch < 0:
      turtle.direction.pitch += 360
  _draw_turtle()

def down(degrees):
  up(-1 * degrees)
