import unittest, os, sys

this_dir = os.path.dirname(os.path.realpath(__file__))
mcgamedata_relative_path = os.path.join(this_dir, "../../mcgamedata")
turtle_path = os.path.join(this_dir, "../")

sys.path.append(mcgamedata_relative_path)
sys.path.append(turtle_path)

from oogway.turtle import init, chat, begin, forward, up, right, left, \
    pen_down, pen_up, delay, down, living_things, start_task, reset_task
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

    def getTilePos(self):
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

class TestUnit(unittest.TestCase):
    def setUp(self):
        game = FakeMcpi(FakeMcpiPlayer(3, Vector(100,200,300)))

        def connect():
            return game

        slept = []
        def fake_sleep(interval):
            slept.append(interval)

        self.game = game
        self.connect = connect
        self.slept = slept

        init(self.connect, "papadapadapa")

        def begin_for_testing(start_distance_from_player=0):
            begin(start_distance_from_player=start_distance_from_player,
                default_trail=[block.GOLD_BLOCK],
                sleep_function=fake_sleep)

        self.begin_for_testing = begin_for_testing

    def test_chat(self):
        chat("hi")
        chat("there")
        self.assertEqual(["hi", "there"], self.game.chat_log)

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

    def test_forward(self):
        self.begin_for_testing()
        forward()
        forward()

        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): "gold_block",
            (100,200,302): ("piston", {"facing":"south"})
        }, self.game.tiles)

    def test_delay(self):
        self.begin_for_testing()
        delay(1)
        forward()
        forward()
        delay(2)
        forward()

        self.assertEqual([1,1,2], self.slept)

    def test_right_90(self):
        self.begin_for_testing()
        forward()
        right(90)

        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): ("piston", {"facing":"west"})
        }, self.game.tiles)

        forward()
        forward()

        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): "gold_block",
            ( 99,200,301): "gold_block",
            ( 98,200,301): ("piston", {"facing":"west"})
        }, self.game.tiles)

    def test_left_90(self):
        self.begin_for_testing()
        forward()
        left(90)

        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): ("piston", {"facing":"east"})
        }, self.game.tiles)

        forward()
        forward()

        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): "gold_block",
            (101,200,301): "gold_block",
            (102,200,301): ("piston", {"facing":"east"})
        }, self.game.tiles)

    def test_up_90(self):
        self.begin_for_testing()
        forward()
        up(90)

        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): ("piston", {"facing":"up"})
        }, self.game.tiles)

        forward()
        forward()

        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): "gold_block",
            (100,201,301): "gold_block",
            (100,202,301): ("piston", {"facing":"up"})
        }, self.game.tiles)

    def test_down_90(self):
        self.begin_for_testing()
        forward()
        down(90)

        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): ("piston", {"facing":"down"})
        }, self.game.tiles)

        forward()
        forward()

        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): "gold_block",
            (100,199,301): "gold_block",
            (100,198,301): ("piston", {"facing":"down"})
        }, self.game.tiles)

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
        forward()
        forward()
        forward()
        forward()

        self.assertEqual({
            (100,200,300): "gold_block",
            (101,200,301): "gold_block",
            (102,200,302): ("piston", {"facing":"south"})
        }, self.game.tiles)

    def test_turn_22_degrees(self):
        self.begin_for_testing()
        left(22)
        forward()
        forward()
        forward()
        forward()
        forward()
        forward()

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
        forward()
        forward()
        pen_up()
        forward()
        forward()
        pen_down(block.GOLD_BLOCK)
        forward()
        forward()

        self.assertEqual({
            (100,200,300): "gold_block",
            (100,200,301): "gold_block",
            (100,200,302): "air",
            (100,200,303): "air",
            (100,200,304): "gold_block",
            (100,200,305): "gold_block",
            (100,200,306): ("piston", {"facing":"south"})
        }, self.game.tiles)

    def test_show_that_pen_up_is_currently_destructive(self):

        # future: enhance the library so that this isn't destructive

        self.begin_for_testing()
        forward()
        forward()
        forward()

        self.begin_for_testing()
        pen_up()
        forward()

        self.assertEqual({
            (100,200,300): "air",
            (100,200,301): ("piston", {"facing":"south"}), # the second turtle, overwriting the first path
            (100,200,302): "gold_block",
            (100,200,303): ("piston", {"facing":"south"}) # the original turtle
        }, self.game.tiles)

    def test_spawn_entity(self):
        self.begin_for_testing()
        pen_down(living.OCELOT)
        forward()
        forward()

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
        forward()
        forward()

        self.assertEqual([
            (living.OCELOT, "uuid1"),
            (living.OCELOT, "uuid2")
        ], living_things())

    def test_living_entity_tasks(self):
        self.begin_for_testing()
        pen_down(living.OCELOT)
        forward()
        forward()
        pen_down(living.WOLF)
        forward()

        self.assertEqual([
            (living.OCELOT, "uuid1"),
            (living.OCELOT, "uuid2"),
            (living.WOLF, "uuid3")
        ], living_things())

        start_task(living.OCELOT.SIT)

        self.assertEqual([
            ("uuid1", "sit"),
            ("uuid2", "sit")
        ], self.game.entity.tasks_in_progress) # by default, only ocelots are selected

        reset_task(living.OCELOT.SIT)

        self.assertEqual([], self.game.entity.tasks_in_progress)

if __name__ == '__main__':
    unittest.main()
