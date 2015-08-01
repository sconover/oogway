import math

    # # advance in the y-only direction one step, then advance once diagonally (+x and +y). repeat.

    # angle = 23

    # absolute_x_pos = 100
    # absolute_y_pos = 100
    # self.assertEqual((0, 1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    # absolute_x_pos = 100
    # absolute_y_pos = 101
    # self.assertEqual((1, 1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    # absolute_x_pos = 101
    # absolute_y_pos = 102
    # self.assertEqual((0, 1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

    # absolute_x_pos = 101
    # absolute_y_pos = 103
    # self.assertEqual((1, 1), calculate_increment_2d((absolute_x_pos, absolute_y_pos), angle))

def calculate_increment_2d(absolute_position, angle_in_degrees, move_distance=1):
    absolute_x = absolute_position[0]
    absolute_y = absolute_position[1]

    adjacent = move_distance
    opposite = math.tan(math.radians(angle_in_degrees)) / adjacent

    x_diff = 0
    y_diff = move_distance

    total_steps_before_increment = int(move_distance / opposite)
    if absolute_y % total_steps_before_increment == total_steps_before_increment - 1:
        return (move_distance, move_distance)
    else:
        return (0, move_distance)

