import math

def calculate_increment_2d(absolute_position, angle_in_degrees, move_distance=1):
  absolute_x = absolute_position[0]
  absolute_y = absolute_position[1]

  if angle_in_degrees <= 45:
    adjacent = move_distance
    opposite = math.tan(math.radians(angle_in_degrees)) / adjacent
    total_steps_before_increment = int(move_distance / opposite)

    if absolute_y % total_steps_before_increment == total_steps_before_increment - 1:
      return (move_distance, move_distance)
    else:
      return (0, move_distance)
  elif angle_in_degrees <= 90:
    adjacent = move_distance
    opposite = math.tan(math.radians(90 - angle_in_degrees)) / adjacent
    total_steps_before_increment = int(move_distance / opposite)

    if absolute_x % total_steps_before_increment == total_steps_before_increment - 1:
      return (move_distance, move_distance)
    else:
      return (move_distance, 0)
  elif angle_in_degrees <= 135:
    adjacent = move_distance
    opposite = math.tan(math.radians(angle_in_degrees - 90)) / adjacent
    total_steps_before_increment = int(move_distance / opposite)

    if absolute_x % total_steps_before_increment == total_steps_before_increment - 1:
      return (move_distance, -1 * move_distance)
    else:
      return (move_distance, 0)
  elif angle_in_degrees <= 180:
    adjacent = move_distance
    opposite = math.tan(math.radians(180 - angle_in_degrees)) / adjacent
    total_steps_before_increment = int(move_distance / opposite)

    if absolute_y % total_steps_before_increment == total_steps_before_increment - 1:
      return (move_distance, -1 * move_distance)
    else:
      return (0, -1 * move_distance)
  elif angle_in_degrees <= 225:
    adjacent = move_distance
    opposite = math.tan(math.radians(angle_in_degrees - 180)) / adjacent
    total_steps_before_increment = int(move_distance / opposite)

    if absolute_y % total_steps_before_increment == total_steps_before_increment - 1:
      return (-1 * move_distance, -1 * move_distance)
    else:
      return (0, -1 * move_distance)
  elif angle_in_degrees <= 270:
    adjacent = move_distance
    opposite = math.tan(math.radians(270 - angle_in_degrees)) / adjacent
    total_steps_before_increment = int(move_distance / opposite)

    if absolute_x % total_steps_before_increment == total_steps_before_increment - 1:
      return (-1 * move_distance, -1 * move_distance)
    else:
      return (-1 * move_distance, 0)
  elif angle_in_degrees <= 315:
    adjacent = move_distance
    opposite = math.tan(math.radians(angle_in_degrees - 270)) / adjacent
    total_steps_before_increment = int(move_distance / opposite)

    if absolute_x % total_steps_before_increment == total_steps_before_increment - 1:
      return (-1 * move_distance, move_distance)
    else:
      return (-1 * move_distance, 0)
  elif angle_in_degrees <= 360:
    adjacent = move_distance
    opposite = math.tan(math.radians(360 - angle_in_degrees)) / adjacent
    total_steps_before_increment = int(move_distance / opposite)

    if absolute_y % total_steps_before_increment == total_steps_before_increment - 1:
      return (-1 * move_distance, move_distance)
    else:
      return (0, move_distance)
