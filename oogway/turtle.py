"""oogway: a python library for doing turtle graphics in Minecraft.

It depends on mcgamedata, which contains metadata about
minecraft objects, like blocks and living things, that
oogway can use to create in a minecraft world, via pen_down().

Oogway requires a specially modified version of the
Sponge Minecraft server, and a special version of the mcpi
client library, which oogway uses to communicate with the
server.

Style stays as close to the original LOGO turtle graphics as
possible (see chapter 3 of Seymour Papert's book, Mindstorms).

Newcomers will learn by bumping into problems: so, error checking
is indended to be robust and error messages are helpful and
intended to be in relatively informal, everyday english.

This library, along with mcgamedata, mcpi mods, Sponge server
mods, and the mcplaygrounds systems automation project, was
written in order to teach a Minecraft+Python intro programming
class to 10-year-olds.

Code samples are verified as part of the unit_test.py test run
(including the picture of the turtle below).

>>> def polygon(sides, side_length):
...     degrees = 360/sides
...     for _ in xrange(sides):
...         right(degrees)
...         forward(side_length)
>>> begin()
>>> pen_down(block.EMERALD_BLOCK)
>>> polygon(6, 12)                 # shell
>>> back(8)
>>> polygon(4, 4)                  # neck
>>> right(90)
>>> forward(4)
>>> right(90)
>>> forward(2)
>>> right(180)
>>> polygon(24, 1)                 # head
>>> pen_up()
>>> forward(11)
>>> left(90)
>>> forward(11)
>>> pen_down(block.EMERALD_BLOCK)
>>> right(45)
>>> polygon(3, 7)                  # front-left foot
>>> right(45)
>>> back(1)
>>> pen_up()
>>> forward(20)
>>> pen_down(block.EMERALD_BLOCK)
>>> right(135)
>>> polygon(3, 7)                  # front-right foot
>>> left(45)
>>> forward(1)
>>> pen_up()
>>> forward(5)
>>> pen_down(block.EMERALD_BLOCK)
>>> forward(1)
>>> left(180)
>>> polygon(3, 5)                  # back-right foot
>>> left(90)
>>> forward(1)
>>> pen_up()
>>> forward(18)
>>> pen_down(block.EMERALD_BLOCK)
>>> left(180)
>>> polygon(3, 5)                  # back-left foot
>>> get_tiles()
            E E
        E E   E                   E E E E
    E E       E   E E E     E E E       E
      E E     E E       E E E
          E E E             E E       E
        E E   v               E E     E
    E E                           E E E
  E                                 E E E
E                                         E
E                                         E
E                                         E           E E E E
E                                         E         E         E
E                                         E E E E E           E
E                                         E       E             E
E                                         E                     E
E                                         E       E             E
E                                         E E E E E           E
E                                         E         E         E
E                                         E           E E E E
E                                         E
E E                                     E E
  E E                               E E
      E E                       E E E E E
          E E                 E E       E
    E E E E E E E           E           E
      E     E   E E   E E     E       E
      E   E         E           E     E
        E E                       E   E
        E                           E
"""

import sys, os
from mcgamedata import block, block_definition, block_property, living, living_definition
from collections import namedtuple
from time import sleep
from sphere_math import calculate_point_on_sphere2
from orientation import Position, Direction

class TurtleSession():
    def __init__(self, position, direction, default_trail, sleep_function):
        self.position = position
        self.direction = direction
        if "TEST" in os.environ:
            self.delay = 0
        else:
            self.delay = 0.1
        self.trail = default_trail
        self.sleep = sleep_function
        self.living_things_selected = {}
        self.tiles = {}

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

    def get_then_set_block(self, x, y, z, gamedata_block, *gamedata_properties):
        property_to_value = {}
        for p in gamedata_properties:
            p.add_to_dict(property_to_value)

        # cast to int. we're mapping a continuous space of very high precision,
        # on to a grid.
        return BlockResult.from_api_block_result(self._m().getThenSetBlockV2(int(x), int(y), int(z), gamedata_block.name, **property_to_value))

    # TODO: check position, raise exception if out of bounds. If this exception is raised, there is a bug somewhere.

    def get_block(self, x, y, z):
        # cast to int. we're mapping a continuous space of very high precision,
        # on to a grid.
        return BlockResult.from_api_block_result(self._m().getBlockV2(int(x), int(y), int(z)))

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
        vec = self._m().player.getTilePosV2(self._m().player.name)
        return Position(vec.x, vec.y, vec.z)

    def chat(self, message):
        self._m().postToChat(message)
        return ChatResult(message)

class BlockResult():
    @staticmethod
    def from_api_block_result(block_info):
        block_def = block.from_block_type_name(block_info["type"])
        block_properties = []
        if "properties" in block_info:
            for k in sorted(block_info["properties"]):
                block_properties.append(block_def.get_property(k).get_value_by_str(block_info["properties"][k]))
        return BlockResult(block_def, *block_properties)

    def __init__(self, block_definition, *block_properties):
        self.definition = block_definition
        self.properties = list(block_properties)

    def __eq__(self, other):
        if isinstance(other, block_definition.BlockDefinition):
            return other == self.definition
        else:
            return other.definition == self.definition

    def __str__(self):
        # TODO: friendlier
        parts = [self.definition.short_usage_str]
        parts.extend(map(lambda p: self.definition.short_usage_str + "." + p.value_str, self.properties))
        return ",".join(parts)

    def __repr__(self):
        return str(self)

class ChatResult():
    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return "[was broadcast to all players] " + self.message

class TilesResult():
    def __init__(self, tiles):
        self.tiles = tiles

    def __repr__(self):
        min_x = sys.maxint
        min_z = sys.maxint
        max_x = 0
        max_z = 0
        for coord in self.tiles:
            min_x = int(min(min_x, coord[0]))
            max_x = int(max(max_x, coord[0]))
            min_z = int(min(min_z, coord[2]))
            max_z = int(max(max_z, coord[2]))

        xz = [None] * (max_z-min_z+1)
        for coord in self.tiles:
            x_offset = int(coord[0] - min_x)
            z_offset = int(coord[2] - min_z)
            if xz[z_offset] == None:
                xz[z_offset] = [None] * (max_x-min_x+1)

            content = self.tiles[coord]
            block_representation = None
            block_type = content
            if type(block_type) == tuple:
                block_type = block_type[0]
            if block_type is block.PISTON:
                facing = content[1]
                if facing == block.PISTON.FACING_SOUTH:
                    block_representation = "v"
                elif facing == block.PISTON.FACING_NORTH:
                    block_representation = "^"
                elif facing == block.PISTON.FACING_EAST:
                    block_representation = ">"
                elif facing == block.PISTON.FACING_WEST:
                    block_representation = "<"
            elif block_type is block.AIR:
                block_representation = " "
            else:
                block_representation = block_type.name[0].upper()
            xz[z_offset][x_offset] = block_representation

        result = ""
        for z_row in xz:
            row_str = ""
            for x_cell in z_row:
                if len(row_str) > 0:
                    row_str += " "
                if x_cell == None:
                    row_str += " "
                else:
                    row_str += x_cell
            result += row_str.rstrip() + "\n"
        return result.rstrip()

_MC = Minecraft()

name_to_block = {}
for block_type in block.ALL:
    name_to_block[block_type.name] = block_type

name_to_living = {}
for living_type in living.ALL:
    name_to_living[living_type.name] = living_type

def _get_turtle_session():
    assert _MC.turtle_session is not None, \
        "Oops, there's no current turtle! You probably need to create a new turtle using the function:\n\nbegin()"

    return _MC.turtle_session

def init(mcpi_minecraft_connect_function, player=None):
    """Start a new minecraft turtle session.
    """
    _MC.mcpi_minecraft_connect_function = mcpi_minecraft_connect_function
    if player:
        _MC.player_name = player
    if _MC.is_connected():
        _MC.reconnect()

    _MC.turtle_session = None

def _check_message(message, call_wont_work_message, try_this_message):
    assert isinstance(message, str) and len(message) > 0 and len(message) <= 10000, \
        "{} The message must be a string, and not too long.".format(call_wont_work_message) + " " + try_this_message

def chat(message):
    """Broadcast a message to all minecraft players.

    >>> chat("hi everyone")
    [was broadcast to all players] hi everyone
    """

    _check_message(message, "Oops, chat({}) won't work.".format(message), "Try this:\n\nchat(\"hello world\")")

    return _MC.chat(message)

def begin(start_distance_from_player=5, default_trail=[block.GOLD_BLOCK], sleep_function=sleep):
    """Create a new turtle, about 5 blocks out from where the player is facing.

    >>> begin()
    >>> get_tiles()
    v
    """
    pos = _MC.get_player_tile_pos()
    rotation_degrees = _MC.get_player_rotation_degrees()

    if rotation_degrees < 0:
        rotation_degrees = 360 + rotation_degrees

    horizon_pitch = 0

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
    position_diff = calculate_point_on_sphere2(direction=Direction(yaw, horizon_pitch, 0), radius=start_distance_from_player)

    start_x = pos.x + position_diff.x
    start_y = pos.y + position_diff.y
    start_z = pos.z + position_diff.z
    _MC.turtle_session = TurtleSession(
        Position(start_x, start_y, start_z),
        Direction(yaw, horizon_pitch, 0),
        default_trail,
        sleep_function)
    return _draw_turtle()

def get_tiles():
    turtle = _get_turtle_session()
    return TilesResult(turtle.tiles)

def _draw_turtle():
    turtle = _get_turtle_session()

    if not turtle.position.is_possible_in_a_minecraft_world():
        return

    previous_block = _MC.get_then_set_block(
        turtle.position.x, turtle.position.y, turtle.position.z,
        block.PISTON, _turtle_facing())
    turtle.tiles[(turtle.position.x, turtle.position.y, turtle.position.z)] = (block.PISTON, _turtle_facing())
    if "DOCTEST" in os.environ and os.environ["DOCTEST"] == "true":
        # this is a hack that makes it so doctests don't fail because of non-None result from begin, forward, and back
        return None
    else:
        return previous_block

def _facing_based_on_yaw(yaw):
    facing = None
    if yaw >= 0:
        facing = block.PISTON.FACING_NORTH
    if yaw >= 45:
        facing = block.PISTON.FACING_EAST
    if yaw >= 135:
        facing = block.PISTON.FACING_SOUTH
    if yaw >= 225:
        facing = block.PISTON.FACING_WEST
    if yaw >= 315:
        facing = block.PISTON.FACING_NORTH

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
    turtle = _get_turtle_session()

    facing_from_yaw = _facing_based_on_yaw(turtle.direction.yaw)
    facing = facing_from_yaw

    if turtle.direction.pitch >= 0:
        facing = _opposite_facing(facing_from_yaw)
    if turtle.direction.pitch >= 45:
        facing = block.PISTON.FACING_DOWN
    if turtle.direction.pitch >= 135:
        facing = facing_from_yaw
    if turtle.direction.pitch >= 225:
        facing = block.PISTON.FACING_UP
    if turtle.direction.pitch >= 315:
        facing = _opposite_facing(facing_from_yaw)

    return facing

def _draw_thing(position, *args):
    turtle = _get_turtle_session()

    if not position.is_possible_in_a_minecraft_world():
        return

    if isinstance(args[0], block_definition.BlockDefinition):
        _MC.set_block(
            position.x, position.y, position.z,
            *args)
        turtle.tiles[(position.x, position.y, position.z)] = tuple(args)
    elif isinstance(args[0], living_definition.LivingDefinition):
        entity = _MC.spawn_entity(
            position.x, position.y, position.z,
            args[0])
        _select_entity(entity)
        _draw_thing(position, block.AIR)
    else:
        raise Exception("don't know what to do with " + str(args))

def _select_entity(entity):
    turtle = _get_turtle_session()
    if entity.type in name_to_living:
        turtle.living_things_selected[entity.uuid] = name_to_living[entity.type]
    else:
        turtle.living_things_selected[entity.uuid] = None

def _move(x,y,z, is_last_move):
    turtle = _get_turtle_session()
    turtle.sleep(turtle.delay)
    a = turtle.position
    b = Position(x,y,z)

    turtle.position = b
    _draw_thing(a, *turtle.trail)
    if turtle.delay > 0.01 or is_last_move:
        return _draw_turtle()
    else:
        return None

def _move_relative(x_diff, y_diff, z_diff, is_last_move):
    turtle = _get_turtle_session()
    return _move(
            turtle.position.x + x_diff,
            turtle.position.y + y_diff,
            turtle.position.z + z_diff,
            is_last_move)

def _is_number(x):
    return isinstance(x, (int, long, float, complex))

min_delay = 0
max_delay = 10

def _check_delay_seconds(delay_seconds, call_wont_work_message, try_this_message):
    assert _is_number(delay_seconds) and delay_seconds >= min_delay and delay_seconds <= max_delay, \
        "{} Delay seconds must be a number of seconds (such as 0.1 or 3) between {} and {}.".format(
            call_wont_work_message,
            min_delay,
            max_delay) + " " + try_this_message

def delay(seconds):
    """Duration of pause, in seconds, between turtle moves.

    Slowing down the turtle is useful to see exactly what the turtle is
    doing, especially when you're "debugging" - or, trying to figure out
    why something you've done isn't working. A good delay in a situation
    like this is a half-second:

    delay(0.5)

    On the other hand, if you're confident that a program is doing what
    you expect it to do, you may not want to wait around. You might want
    to have no delay at all:

    delay(0)

    By default, the delay is one tenth of a second:

    delay(0.1)
    """
    _check_delay_seconds(seconds, "Oops, delay({}) won't work.".format(str(seconds)), "Try this:\n\ndelay(0.5)")

    _get_turtle_session().delay = seconds

min_distance = 1
max_distance = 1000

def _check_distance(distance, call_wont_work_message, try_this_message):
    assert isinstance(distance, int) and distance >= min_distance and distance <= max_distance, \
        "{} Distance must be a whole number between {} and {}.".format(
            call_wont_work_message,
            min_distance,
            max_distance) + " " + try_this_message

def forward(distance):
    """Move the turtle forward a given distance (in its current direction).

    Distance must be a whole number between {} and {}.

    >>> begin()
    >>> forward(2)
    >>> get_tiles()
    G
    G
    v
    """.format(min_distance, max_distance)

    _check_distance(distance, "Oops, forward({}) won't work.".format(distance), "Try this:\n\nforward(3)")

    turtle = _get_turtle_session()

    # all moves forward except the last one
    for i in xrange(distance-1):
        position_diff = calculate_point_on_sphere2(direction=turtle.direction, radius=1)
        _move_relative(position_diff.x, position_diff.y, position_diff.z, False)

    # last forward move
    position_diff = calculate_point_on_sphere2(direction=turtle.direction, radius=1)
    return _move_relative(position_diff.x, position_diff.y, position_diff.z, True)

def back(distance):
    """Move the turtle backward a given distance (opposite of its current direction).

    Distance must be a whole number between {} and {}.

    >>> begin()
    >>> back(2)
    >>> get_tiles()
    ^
    G
    G
    """.format(min_distance, max_distance)

    _check_distance(distance, "Oops, back({}) won't work.".format(distance), "Try this:\n\nback(3)")

    right(180)
    return forward(distance)

block_names = sorted(map(lambda l: str(l), block.ALL))
all_blocks_str = ", ".join(block_names)
all_living_things_str = ", ".join(sorted(map(lambda l: str(l), living.ALL)))

all_block_types_with_property_values = {}

for block_def in block.ALL:
    all_block_types_with_property_values[str(block_def)] = map(lambda p: map(lambda v: str(v), p.all_values), block_def.ALL_PROPERTIES)

all_block_types_with_property_values_str = ""
for block_name in block_names:
    if len(all_block_types_with_property_values_str)>0:
        all_block_types_with_property_values_str += "\n\n"
    all_block_types_with_property_values_str += block_name + ": \n"
    value_groups = all_block_types_with_property_values[block_name]
    for value_group in value_groups:
        all_block_types_with_property_values_str += ", ".join(value_group) + "\n"

def pen_down(*args):
    """Change the type of trail the turtle is leaving behind. When the turtle
    moves forward or back, it will leave this thing behind.

    The first argument must be a type of block, or a type of living thing.

    Example: pen_down(block.STONE)
    Example: pen_down(living.OCELOT)

    The rest of the arguments may be any number of property values for a block type.

    Example: pen_down(block.FLOWER_POT, block.FLOWER_POT.CONTENTS_BLUE_ORCHID)

    TODO: see mcgamedata for details on block and living

    >>> begin()
    >>> forward(2)
    >>> pen_down(block.STONE)
    >>> forward(2)
    >>> get_tiles()
    G
    G
    S
    S
    v
    """

    if len(args) == 0 or args[0] not in block.ALL and args[0] not in living.ALL:
        raise AssertionError(
            "Oops, pen_down(" + ", ".join(map(lambda a: str(a), args)) + ") won't work. " + \
            "Trail must be a type of block, or a type of living thing, along with any properties.\n\n" + \
            "Example 1: pen_down(block.GOLD_BLOCK)\n\n" + \
            "Example 2: pen_down(block.FLOWER_POT, block.FLOWER_POT.CONTENTS_BLUE_ORCHID)\n\n" + \
            "Here are all the types of blocks:\n" + \
            "".join(sorted(map(lambda b: "    " + str(b) + "\n", block.ALL))) + \
            "\nHere are all the types of living things:\n" + \
            "".join(sorted(map(lambda l: "    " + str(l) + "\n", living.ALL))) +
            "\n\nTry this:\n\npen_down(block.GOLD_BLOCK)")

    if len(args) > 1:
        the_type = args[0]
        value_args = args[1:]

        if len(filter(lambda v: isinstance(v, block_property.PropertyWithValue) and \
            v.block_property in the_type.ALL_PROPERTIES, value_args)) != len(value_args):
            all_values_str = ""
            for p in the_type.ALL_PROPERTIES:
                all_values_str += "\n"
                for v in p.all_values:
                    all_values_str += "    " + str(v) + "\n"

            raise AssertionError(
                "Oops, pen_down(" + ", ".join(map(lambda a: str(a), args)) + ") won't work, because " + \
                ", ".join(map(lambda v: str(v), filter(lambda v: not isinstance(v, block_property.PropertyWithValue) or v.block_property not in the_type.ALL_PROPERTIES, value_args))) + \
                " not part of block type " + str(the_type) + "\n\n" + \
                "Here are all the property values you can use with block type " + str(the_type) + ":\n" + all_values_str + \
                "\n\nTry this:\n\npen_down(block.FLOWER_POT, block.FLOWER_POT.CONTENTS_BLUE_ORCHID)")

    turtle = _get_turtle_session()
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
def pen_up():
    """Change the type of trail the turtle is leaving behind to be air blocks.

    >>> begin()
    >>> forward(2)
    >>> pen_up()
    >>> forward(2)
    >>> get_tiles()
    G
    G
    <BLANKLINE>
    <BLANKLINE>
    v
    """
    turtle = _get_turtle_session()
    turtle.trail = [block.AIR] # this is destructive.

def living_things():
    turtle = _get_turtle_session()
    return turtle.living_things_selected

def _select_all_living_of_type(task, entities):
    return filter(lambda entity_uuid: entities[entity_uuid] == name_to_living[task.entity_name], entities)

def start_task(task, selector=_select_all_living_of_type):
    def all_tasks_at_once(mc):
        for entity_uuid in _select_all_living_of_type(task, living_things()):
            mc.living_entity_start_task(entity_uuid, task)
    _MC.batch(all_tasks_at_once)

def reset_task(task, selector=_select_all_living_of_type):
    def all_tasks_at_once(mc):
        for entity_uuid in _select_all_living_of_type(task, living_things()):
            mc.living_entity_reset_task(entity_uuid, task)
    _MC.batch(all_tasks_at_once)

def current_position():
    return _MC.get_player_tile_pos()

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
    results = _MC.get_all_entities_in_bounding_box(cube_corners[0], cube_corners[1])
    for entity in results:
        _select_entity(entity)

# select_living_things(cube_from_point(current_position(), HORIZON_DISTANCE)))

# path of blocks
#    what if it's sand and the sand falls?

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
#     is_not(block.AIR) ... predicate defs return curried functions
# both, neither, either
# ...good way to teach predicate logic

def _check_degrees(degrees, call_wont_work_message, try_this_message):
    assert _is_number(degrees), "{} Degrees must be a number.".format(call_wont_work_message) + " " + try_this_message

def right(degrees):
    """Turn the turtle to the right, the given number of degrees.

    A complete turn (a circle) has 360 degrees, so:
    - 90 degrees is a "right turn"
    - 180 degrees (a half circle) turns the turtle around
    - 270 degrees (3/4th of a circle) turns the turtle around so that
      she is actually making a "left turn".
    - 360 degrees (a whole circle) turns the turtle all the way around,
      which points her in the same direction as before.
    - 45 degrees is a right-diagonal move (between straight forward and a right turn)

    Degrees must be a number.

    >>> begin()
    >>> forward(2)
    >>> right(90) # face right
    >>> forward(2)
    >>> get_tiles()
        G
        G
    < G G

    >>> begin()
    >>> forward(2)
    >>> right(180) # face backwards
    >>> forward(2)
    >>> get_tiles()
    ^
    G
    G

    >>> begin()
    >>> forward(2)
    >>> right(270) # face left (!)
    >>> forward(2)
    >>> get_tiles()
    G
    G
    G G >

    >>> begin()
    >>> forward(2)
    >>> right(360) # ...turn ALL the way around, meaning she's back facing the same direction as before
    >>> forward(2)
    >>> get_tiles()
    G
    G
    G
    G
    v

    >>> begin()
    >>> forward(1)
    >>> right(45) # ...move in a diagonal (right/front)
    >>> forward(2)
    >>> get_tiles()
        G
      G G
    <
    """
    _check_degrees(degrees, "Oops, right({}) won't work.".format(degrees), "Try this:\n\nright(90)")

    turtle = _get_turtle_session()

    turtle.direction.yaw += degrees
    turtle.direction.yaw = turtle.direction.yaw % 360

    _draw_turtle()

def left(degrees):
    _check_degrees(degrees, "Oops, left({}) won't work.".format(degrees), "Try this:\n\nleft(90)")

    right(-1 * degrees)

def up(degrees):
    _check_degrees(degrees, "Oops, up({}) won't work.".format(degrees), "Try this:\n\nup(90)")

    turtle = _get_turtle_session()

    turtle.direction.pitch -= degrees
    turtle.direction.pitch = turtle.direction.pitch % 360

    _draw_turtle()

def down(degrees):
    _check_degrees(degrees, "Oops, down({}) won't work.".format(degrees), "Try this:\n\ndown(90)")

    up(-1 * degrees)

def peek():
    turtle = _get_turtle_session()
    position_diff = calculate_point_on_sphere2(direction=turtle.direction, radius=1)
    peek_x = turtle.position.x + position_diff.x
    peek_y = turtle.position.y + position_diff.y
    peek_z = turtle.position.z + position_diff.z

    if Position(peek_x, peek_y, peek_z).is_possible_in_a_minecraft_world():
        return _MC.get_block(
            turtle.position.x + position_diff.x,
            turtle.position.y + position_diff.y,
            turtle.position.z + position_diff.z)
    else:
        return None
