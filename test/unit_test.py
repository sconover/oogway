import unittest, doctest, os, sys, re

this_dir = os.path.dirname(os.path.realpath(__file__))
mcgamedata_relative_path = os.path.join(this_dir, "../../mcgamedata")
turtle_path = os.path.join(this_dir, "../")

sys.path.append(mcgamedata_relative_path)
sys.path.append(turtle_path)

import oogway.turtle
from oogway.turtle import init, chat, begin, forward, back, up, right, left, \
    pen_down, pen_up, delay, down, living_things, start_task, reset_task, TilesResult
from mcgamedata import block, living

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

    def getTilePosV2(self, player_name):
        return self.tile_pos

class EntitySpawnResult():
    def __init__(self, entity_type_name, uuid):
        self.type = entity_type_name
        self.uuid = uuid

class FakeMcpiEntity():
    def __init__(self):
        self.entities_created = []
        self.tasks_in_progress = []

    def spawnV2(self, x, y, z, entity_type_name, **property_to_value):
        if property_to_value == {}:
            self.entities_created.append((x,y,z,entity_type_name))
        else:
            self.entities_created.append((x,y,z,entity_type_name, property_to_value))
        return EntitySpawnResult(entity_type_name, "uuid" + str(len(self.entities_created)))

    def startTaskV2(self, entity_uuid, task_name):
        self.tasks_in_progress.append((entity_uuid, task_name))

    def resetTaskV2(self, entity_uuid, task_name):
        for entry in self.tasks_in_progress:
            if entry == (entity_uuid, task_name):
                self.tasks_in_progress.remove(entry)
                break

class FakeMcpi():
    def __init__(self, player):
        self.player = player
        self.entity = FakeMcpiEntity()
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

    def startBatch(this):
        pass

    def endBatch(this):
        pass

# extracted so we can reuse with doctests
def setupTest(targetTestInstance):
    game = FakeMcpi(FakeMcpiPlayer(3, Vector(100,200,300)))

    def connect():
        return game

    slept = []
    def fake_sleep(interval):
        slept.append(interval)

    targetTestInstance.game = game
    targetTestInstance.connect = connect
    targetTestInstance.slept = slept

    init(targetTestInstance.connect, "papadapadapa")

    def begin_for_testing(start_distance_from_player=0):
        begin(start_distance_from_player=start_distance_from_player,
            default_trail=[block.GOLD_BLOCK],
            sleep_function=fake_sleep)

    targetTestInstance.begin_for_testing = begin_for_testing

class TestUnit(unittest.TestCase):
    def setUp(self):
        setupTest(self)

    def test_chat(self):
        chat("hi")
        chat("there")
        self.assertEqual(["hi", "there"], self.game.chat_log)

    def test_valid_chat(self):
        with self.assertRaisesRegexp(AssertionError, "Oops, chat\(1\) won't work. The message must be a string, and not too long."):
            chat(1)

        with self.assertRaisesRegexp(AssertionError, "Oops, chat\(\) won't work. The message must be a string, and not too long."):
            chat("")

        with self.assertRaisesRegexp(AssertionError, "Oops, chat\(" + ("X" * 20000) + "\) won't work. The message must be a string, and not too long."):
            chat("X" * 20000)

    def test_begin_the_begin(self):
        self.game.player.tile_pos = Vector(100,200,300)
        self.game.player.rotation = 2
        self.begin_for_testing(start_distance_from_player=5)
        self.assertEqual({(100,200,305):("piston", {"facing":"south"})}, self.game.tiles)

        self.game.reset()
        self.game.player.tile_pos = Vector(100,200,300)
        self.game.player.rotation = 92
        self.begin_for_testing(start_distance_from_player=5)
        self.assertEqual({(95,200,300):("piston", {"facing":"west"})}, self.game.tiles)

        self.game.reset()
        self.game.player.tile_pos = Vector(100,200,300)
        self.game.player.rotation = 182
        self.begin_for_testing(start_distance_from_player=5)
        self.assertEqual({(100,200,295):("piston", {"facing":"north"})}, self.game.tiles)

        self.game.reset()
        self.game.player.tile_pos = Vector(100,200,300)
        self.game.player.rotation = 272
        self.begin_for_testing(start_distance_from_player=5)
        self.assertEqual({(105,200,300):("piston", {"facing":"east"})}, self.game.tiles)

    def test_not_begun(self):
        with self.assertRaisesRegexp(AssertionError, re.compile("Oops, there's no current turtle.*", re.MULTILINE)):
            forward(1)

    def test_forward(self):
        self.begin_for_testing()
        forward(2)

        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): "gold_block",
            (100,200,302): ("piston", {"facing":"south"})
        }, self.game.tiles)

    def test_forward_distance_bounds_and_type(self):
        self.begin_for_testing()

        with self.assertRaisesRegexp(AssertionError, "Oops, forward\(0\) won't work. Distance must be a whole number between 1 and 1000."):
            forward(0)

        with self.assertRaisesRegexp(AssertionError, "Oops, forward\(-1\) won't work. Distance must be a whole number between 1 and 1000."):
            forward(-1)

        with self.assertRaisesRegexp(AssertionError, "Oops, forward\(1001\) won't work. Distance must be a whole number between 1 and 1000."):
            forward(1001)

        with self.assertRaisesRegexp(AssertionError, "Oops, forward\(1.1\) won't work. Distance must be a whole number between 1 and 1000."):
            forward(1.1)

        with self.assertRaisesRegexp(AssertionError, "Oops, forward\(abc\) won't work. Distance must be a whole number between 1 and 1000."):
            forward('abc')

    def test_forward_outside_of_game_boundaries_just_doesnt_attempt_to_lay_blocks__more_than_max_y(self):
        self.game.player.tile_pos = Vector(100,253,300)
        self.game.player.rotation = 2
        self.begin_for_testing(start_distance_from_player=5)

        up(90)
        forward(10)

        self.assertEqual({
            (100,253,305): "gold_block",
            (100,254,305): "gold_block",
            (100,255,305): "gold_block"
        }, self.game.tiles)

    def test_forward_outside_of_game_boundaries_just_doesnt_attempt_to_lay_blocks__less_than_min_y(self):
        self.game.player.tile_pos = Vector(100,2,300)
        self.game.player.rotation = 2
        self.begin_for_testing(start_distance_from_player=5)

        down(90)
        forward(10)

        self.assertEqual({
            (100,2,305): "gold_block",
            (100,1,305): "gold_block",
            (100,0,305): "gold_block"
        }, self.game.tiles)

    def test_back(self):
        self.begin_for_testing()
        back(2)

        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,299): "gold_block",
            (100,200,298): ("piston", {"facing":"north"})
        }, self.game.tiles)

    def test_back_distance_bounds_and_type(self):
        self.begin_for_testing()

        with self.assertRaisesRegexp(AssertionError, "Oops, back\(0\) won't work. Distance must be a whole number between 1 and 1000."):
            back(0)

        with self.assertRaisesRegexp(AssertionError, "Oops, back\(-1\) won't work. Distance must be a whole number between 1 and 1000."):
            back(-1)

        with self.assertRaisesRegexp(AssertionError, "Oops, back\(1001\) won't work. Distance must be a whole number between 1 and 1000."):
            back(1001)

        with self.assertRaisesRegexp(AssertionError, "Oops, back\(1.1\) won't work. Distance must be a whole number between 1 and 1000."):
            back(1.1)

        with self.assertRaisesRegexp(AssertionError, "Oops, back\(abc\) won't work. Distance must be a whole number between 1 and 1000."):
            back('abc')

    def test_delay(self):
        self.begin_for_testing()
        delay(1)
        forward(2)
        delay(2)
        forward(1)

        self.assertEqual([1,1,2], self.slept)

    def test_delay_has_proper_type_and_in_bounds(self):
        self.begin_for_testing()

        with self.assertRaisesRegexp(AssertionError, "Oops, delay\(foo\) won't work\. Delay seconds must be a number of seconds \(such as 0.1 or 3\) between 0 and 10."):
            delay("foo")

        with self.assertRaisesRegexp(AssertionError, "Oops, delay\(11\) won't work\. Delay seconds.*"):
            delay(11)

        with self.assertRaisesRegexp(AssertionError, "Oops, delay\(-1\) won't work\. Delay seconds.*"):
            delay(-1)

    def test_right_90(self):
        self.begin_for_testing()
        forward(1)
        right(90)

        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): ("piston", {"facing":"west"})
        }, self.game.tiles)

        forward(2)

        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): "gold_block",
            ( 99,200,301): "gold_block",
            ( 98,200,301): ("piston", {"facing":"west"})
        }, self.game.tiles)

    def test_right_over_360(self):
        self.begin_for_testing()
        forward(1)
        right(3690)

        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): ("piston", {"facing":"west"})
        }, self.game.tiles)

        forward(2)

        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): "gold_block",
            ( 99,200,301): "gold_block",
            ( 98,200,301): ("piston", {"facing":"west"})
        }, self.game.tiles)

    def test_left_90(self):
        self.begin_for_testing()
        forward(1)
        left(90)

        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): ("piston", {"facing":"east"})
        }, self.game.tiles)

        forward(2)

        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): "gold_block",
            (101,200,301): "gold_block",
            (102,200,301): ("piston", {"facing":"east"})
        }, self.game.tiles)

    def test_up_90(self):
        self.begin_for_testing()
        forward(1)
        up(90)

        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): ("piston", {"facing":"up"})
        }, self.game.tiles)

        forward(2)

        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): "gold_block",
            (100,201,301): "gold_block",
            (100,202,301): ("piston", {"facing":"up"})
        }, self.game.tiles)

    def test_up_over_360(self):
        self.begin_for_testing()
        forward(1)
        up(3690)

        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): ("piston", {"facing":"up"})
        }, self.game.tiles)

        forward(2)

        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): "gold_block",
            (100,201,301): "gold_block",
            (100,202,301): ("piston", {"facing":"up"})
        }, self.game.tiles)

    def test_down_90(self):
        self.begin_for_testing()
        forward(1)
        down(90)

        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): ("piston", {"facing":"down"})
        }, self.game.tiles)

        forward(2)

        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): "gold_block",
            (100,199,301): "gold_block",
            (100,198,301): ("piston", {"facing":"down"})
        }, self.game.tiles)

    def test_show_that_turtle_wont_turn_right_when_going_down_or_up(self):
        self.begin_for_testing()
        forward(2)
        down(90)
        forward(2)
        right(90)
        forward(2)
        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): "gold_block",

            (100,200,302): "gold_block",
            (100,199,302): "gold_block",

            # turtle should have gone right but it didn't.

            (100,198,302): "gold_block",
            (100,197,302): "gold_block",
            (100,196,302): ("piston", {"facing":"down"})
        }, self.game.tiles)

    def test_some_more_turning(self):
        self.begin_for_testing()
        forward(2)
        right(90)
        forward(2)
        down(90)
        forward(2)
        print self.game.tiles
        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): "gold_block",
            (100,200,302): "gold_block",
            (99,200,302): "gold_block",
            (98,200,302): "gold_block",
            (98,199,302): "gold_block",
            (98,198,302): ("piston", {"facing":"down"})
        }, self.game.tiles)

    def test_turn_methods_take_valid_degrees(self):
        self.begin_for_testing()

        with self.assertRaisesRegexp(AssertionError, "Oops, right\(abc\) won't work. Degrees must be a number."):
            right('abc')

        with self.assertRaisesRegexp(AssertionError, "Oops, left\(abc\) won't work. Degrees must be a number."):
            left('abc')

        with self.assertRaisesRegexp(AssertionError, "Oops, up\(abc\) won't work. Degrees must be a number."):
            up('abc')

        with self.assertRaisesRegexp(AssertionError, "Oops, down\(abc\) won't work. Degrees must be a number."):
            down('abc')

    def test_turns_and_piston_facing(self):
        self.begin_for_testing()
        self.assertEqual({(100,200,300): ("piston", {"facing":"south"})}, self.game.tiles)
        right(30)
        self.assertEqual({(100,200,300): ("piston", {"facing":"south"})}, self.game.tiles)
        right(30) # yaw 60
        self.assertEqual({(100,200,300): ("piston", {"facing":"west"})}, self.game.tiles)
        right(30) # yaw 90 - due west
        self.assertEqual({(100,200,300): ("piston", {"facing":"west"})}, self.game.tiles)
        right(30) # yaw 120
        self.assertEqual({(100,200,300): ("piston", {"facing":"west"})}, self.game.tiles)
        right(30) # yaw 150
        self.assertEqual({(100,200,300): ("piston", {"facing":"north"})}, self.game.tiles)
        right(30) # yaw 180 - due north
        self.assertEqual({(100,200,300): ("piston", {"facing":"north"})}, self.game.tiles)
        right(30) # yaw 210
        self.assertEqual({(100,200,300): ("piston", {"facing":"north"})}, self.game.tiles)
        right(30) # yaw 240
        self.assertEqual({(100,200,300): ("piston", {"facing":"east"})}, self.game.tiles)
        right(30) # yaw 270 - due east
        self.assertEqual({(100,200,300): ("piston", {"facing":"east"})}, self.game.tiles)
        right(30) # yaw 300
        self.assertEqual({(100,200,300): ("piston", {"facing":"east"})}, self.game.tiles)
        right(30) # yaw 330
        self.assertEqual({(100,200,300): ("piston", {"facing":"south"})}, self.game.tiles)
        right(30) # yaw 360
        self.assertEqual({(100,200,300): ("piston", {"facing":"south"})}, self.game.tiles)

        up(30) # pitch 60
        self.assertEqual({(100,200,300): ("piston", {"facing":"south"})}, self.game.tiles)
        up(30) # pitch 30
        self.assertEqual({(100,200,300): ("piston", {"facing":"up"})}, self.game.tiles)
        up(30) # pitch 0 - straight up
        self.assertEqual({(100,200,300): ("piston", {"facing":"up"})}, self.game.tiles)
        up(30) # pitch 330
        self.assertEqual({(100,200,300): ("piston", {"facing":"up"})}, self.game.tiles)
        up(30) # pitch 300
        self.assertEqual({(100,200,300): ("piston", {"facing":"north"})}, self.game.tiles)
        up(30) # pitch 270
        self.assertEqual({(100,200,300): ("piston", {"facing":"north"})}, self.game.tiles)
        up(30) # pitch 240
        self.assertEqual({(100,200,300): ("piston", {"facing":"north"})}, self.game.tiles)
        up(30) # pitch 210
        self.assertEqual({(100,200,300): ("piston", {"facing":"down"})}, self.game.tiles)
        up(30) # pitch 180 - straight down
        self.assertEqual({(100,200,300): ("piston", {"facing":"down"})}, self.game.tiles)
        up(30) # pitch 150
        self.assertEqual({(100,200,300): ("piston", {"facing":"down"})}, self.game.tiles)
        up(30) # pitch 120
        self.assertEqual({(100,200,300): ("piston", {"facing":"south"})}, self.game.tiles)
        up(30) # pitch 90
        self.assertEqual({(100,200,300): ("piston", {"facing":"south"})}, self.game.tiles)

    def test_turn_45_degrees(self):
        self.begin_for_testing()
        left(45)
        forward(4)

        self.assertEqual({
            (100,200,300): "gold_block",
            (101,200,301): "gold_block",
            (102,200,302): ("piston", {"facing":"south"})
        }, self.game.tiles)

    def test_turn_22_degrees(self):
        self.begin_for_testing()
        left(22)
        forward(6)

        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): "gold_block",
            (101,200,302): "gold_block",
            (101,200,303): "gold_block",
            (101,200,304): "gold_block",
            (102,200,305): ("piston", {"facing":"south"})
        }, self.game.tiles)

    def test_pen_down_pen_up(self):
        self.begin_for_testing()
        forward(2)
        pen_up()
        forward(2)
        pen_down(block.GOLD_BLOCK)
        forward(2)

        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): "gold_block",
            (100,200,302): "air",
            (100,200,303): "air",
            (100,200,304): "gold_block",
            (100,200,305): "gold_block",
            (100,200,306): ("piston", {"facing":"south"})
        }, self.game.tiles)

    def test_pen_down_invalid_turtle_trail_type(self):
        self.begin_for_testing()

        with self.assertRaisesRegexp(AssertionError, re.compile("Oops, pen_down\(\) won't work\.", re.MULTILINE)):
            pen_down()

        with self.assertRaisesRegexp(AssertionError, re.compile("Trail must be a type of block, or a type of living thing, along with any properties\.", re.MULTILINE)):
            pen_down()

        with self.assertRaisesRegexp(AssertionError, re.compile("^Example 1: pen_down\(block.GOLD_BLOCK\)", re.MULTILINE)):
            pen_down()

        with self.assertRaisesRegexp(AssertionError, re.compile("^Example 2: pen_down\(block\.FLOWER_POT, block\.FLOWER_POT\.CONTENTS_BLUE_ORCHID\)", re.MULTILINE)):
            pen_down()

        with self.assertRaisesRegexp(AssertionError, re.compile("^    block\.GOLD_BLOCK", re.MULTILINE)):
            pen_down()

        with self.assertRaisesRegexp(AssertionError, re.compile("^    living\.OCELOT", re.MULTILINE)):
            pen_down()

        with self.assertRaisesRegexp(AssertionError, re.compile("Oops, pen_down\(foo, bar, 2\) won't work\.", re.MULTILINE)):
            pen_down("foo", "bar", 2)

    def test_pen_down_invalid_turtle_trail_property(self):
        self.begin_for_testing()

        with self.assertRaisesRegexp(AssertionError, re.compile("Oops, pen_down\(block\.FLOWER_POT, block.QUARTZ_STAIRS\.FACING_NORTH\) won't work, " + \
            "because block\.QUARTZ_STAIRS.FACING_NORTH not part of block type block\.FLOWER_POT", re.MULTILINE)):
            pen_down(block.FLOWER_POT, block.QUARTZ_STAIRS.FACING_NORTH)

        with self.assertRaisesRegexp(AssertionError, re.compile("^    block\.FLOWER_POT\.CONTENTS_BLUE_ORCHID", re.MULTILINE)):
            pen_down(block.FLOWER_POT, block.QUARTZ_STAIRS.FACING_NORTH)

        with self.assertRaisesRegexp(AssertionError, re.compile("Oops, pen_down\(block.FLOWER_POT, foo, 1\) won't work, because foo, 1 not part of block type block\.FLOWER_POT", re.MULTILINE)):
            pen_down(block.FLOWER_POT, "foo", 1)

    def test_show_that_pen_up_is_currently_destructive(self):

        # future: enhance the library so that this isn't destructive

        self.begin_for_testing()
        forward(3)

        self.begin_for_testing()
        pen_up()
        forward(1)

        self.assertEqual({
            (100,200,300): "air",
            (100,200,301): ("piston", {"facing":"south"}), # the second turtle, overwriting the first path
            (100,200,302): "gold_block",
            (100,200,303): ("piston", {"facing":"south"}) # the original turtle
        }, self.game.tiles)

    def test_spawn_entity(self):
        self.begin_for_testing()
        pen_down(living.OCELOT)
        forward(2)

        self.assertEqual({
            (100,200,300): "air",
            (100,200,301): "air",
            (100,200,302): ("piston", {"facing":"south"})
        }, self.game.tiles)

        self.assertEqual([
            (100, 200, 300, 'ocelot', {'owner': 'papadapadapa'}),
            (100, 200, 301, 'ocelot', {'owner': 'papadapadapa'})
        ], self.game.entity.entities_created)

    def test_track_spawned_entities(self):
        self.begin_for_testing()
        pen_down(living.OCELOT)
        forward(2)

        self.assertEqual({
            "uuid1": living.OCELOT,
            "uuid2": living.OCELOT
        }, living_things())

    def test_living_entity_tasks(self):
        self.begin_for_testing()
        pen_down(living.OCELOT)
        forward(2)
        pen_down(living.WOLF)
        forward(1)

        self.assertEqual({
            "uuid1": living.OCELOT,
            "uuid2": living.OCELOT,
            "uuid3": living.WOLF
        }, living_things())

        start_task(living.OCELOT.SIT)

        self.assertEqual([
            ("uuid1", "sit"),
            ("uuid2", "sit")
        ], sorted(self.game.entity.tasks_in_progress)) # by default, only ocelots are selected

        reset_task(living.OCELOT.SIT)

        self.assertEqual([], self.game.entity.tasks_in_progress)

    def test_tile_result_repr(self):
        self.assertEqual(
            "^\n" +
            "v", TilesResult({
            (100,200,300): (block.PISTON, block.PISTON.FACING_NORTH),
            (100,200,301): (block.PISTON, block.PISTON.FACING_SOUTH)
        }).__repr__())

        self.assertEqual(
            "G\n" +
            "G\n" +
            "v", TilesResult({
            (100,200,300): (block.GOLD_BLOCK),
            (100,200,301): (block.GOLD_BLOCK),
            (100,200,302): (block.PISTON, block.PISTON.FACING_SOUTH)
        }).__repr__())

        self.assertEqual(
            "G\n" +
            "G G >", TilesResult({
            (100,200,300): (block.GOLD_BLOCK),
            (100,200,301): (block.GOLD_BLOCK),
            (101,200,301): (block.GOLD_BLOCK),
            (102,200,301): (block.PISTON, block.PISTON.FACING_EAST)
        }).__repr__())

        self.assertEqual(
            "    G\n" +
            "< G G", TilesResult({
            (100,200,300): (block.GOLD_BLOCK),
            (100,200,301): (block.GOLD_BLOCK),
            ( 99,200,301): (block.GOLD_BLOCK),
            ( 98,200,301): (block.PISTON, block.PISTON.FACING_WEST)
        }).__repr__())

        self.assertEqual(
            "    G\n" +
            "< G", TilesResult({
            (100,200,300): (block.GOLD_BLOCK),
            (100,200,301): (block.AIR),
            ( 99,200,301): (block.GOLD_BLOCK),
            ( 98,200,301): (block.PISTON, block.PISTON.FACING_WEST)
        }).__repr__())

if __name__ == '__main__':
    os.environ['TEST'] = "true"

    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestUnit))
    suite.addTest(doctest.DocTestSuite(oogway.turtle, setUp=setupTest, optionflags=doctest.ELLIPSIS))
    unittest.TextTestRunner(verbosity=2).run(suite)
