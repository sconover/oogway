from math import sin, cos, radians, tan
from orientation import Position
from logging import getLogger

def calculate_point_on_sphere(direction, radius):
    """
    Given a direction, that has Minecraft pitch and yaw, calculate the
    destination coordinates (x, y, z) on a sphere (imagine standing
    inside of a sphere and pointing to some point on the sphere "surface").

    https://en.wikipedia.org/wiki/Spherical_coordinate_system

    The function first adjusts the pitch and yaw to international conventions,
    as shown at the top of the wikipedia link above.

    It uses the set of equations at the bottom of this section...

    https://en.wikipedia.org/wiki/Spherical_coordinate_system#Cartesian_coordinates

    (direction.yaw is phi, direction.pitch is theta)

    x = radius * sin(theta) * cos(phi)
    y = radius * sin(theta) * sin(phi)
    z = radius * cos(theta)

    ...to calculate the cartesian coordinates on the sphere. It then maps back to
    Minecraft.

    Note that because we do not take into account "roll" - i.e. this is a simplification
    of real-world movement of a rigid object in space - some perhaps-strange movements
    occur. For example, attempting to turn when going straight up or straight down will appear
    to do nothing. That's because even a severe change in yaw will not affect the pitch of the object -
    these vary independently - and the calculation used will "prefer" the pitch orientation.

    In Minecraft:
      - see this thread for more details:
        https://bukkit.org/threads/tutorial-how-to-calculate-vectors.138849/

      Yaw 180 (or -180) degrees is Due North
      Moving North decreases Z (+N = -z)

      Yaw -90 degrees is Due East
      Moving East increases X (+E = +x)

      Yaw 0 degrees is Due South
      Moving South increases Z (+S = +z)

      Yaw +90 degrees is Due West
      Moving West decreases X (+W = -x)

      Pitch 0 degrees is the horizon

      Pitch -90 degrees is straight up (zenith)
      Moving up increases Y (+U = +y)

      Pitch +90 degrees is straight down
      Moving down decreases Y (+D = -y)


    From https://en.wikipedia.org/wiki/Spherical_coordinate_system#Conventions
    "The use of (r, theta, phi) to denote radial distance, inclination (or elevation), and azimuth, respectively,
     is common practice in physics, and is specified by ISO standard 80000-2 :2009, and earlier in ISO 31-11 (1992)."

    So, according to the ISO standard:
    pitch = inclination/elevation/altitude = theta
    yaw = azimuth = phi

    We shall map minecraft values to the following, such that we can employ conventional
    methods of calculating cartesian coordinates from sperical coordinates.

    Roughly, we are going to:
      - "tilt" the ptich such that the zenith is zero degrees
      - adjust degrees such that 0 =< degrees < 360

    In the international convention:
      - The Z axis points "up-down". Imagine
        the earth: the Z axis would pass through the poles, and Z = 0 degrees
        would be the North Pole, and Z=180 degrees would be the South Pole.
      - X and Y axes can be imagined as being in the plane of the Equator.
      - the Prime Meridian (and its antimeridian) is the XZ plane - IRL this runs through Greenwich, England.
      - see also https://en.wikipedia.org/wiki/Axes_conventions
        - especially: https://en.wikipedia.org/wiki/Axes_conventions#/media/File:ECEF_ENU_Longitude_Latitude_relationships.svg

      Yaw/Phi 0 shall be Due North
      Moving North increases X (+N = +x)

      Yaw/Phi 90 degrees is Due East
      Moving East increases Y (+E = +y)

      Yaw/Phi 180 degrees is Due South
      Moving South decreases X (+S = -x)

      Yaw/Phi 270 degrees is Due West
      Moving West decreases Y (+W = -y)

      Pitch/Theta 0 degrees is the zenith
      Moving up increases Z (+U = +z)

      Pitch/Theta 90 degrees is the horizon

      Pitch/Theta 180 degrees is straight down
      Moving down decreases Z (+D = -z)
    """

    log = getLogger(__name__)
    to_log = {}

    minecraft_yaw_degrees = direction.yaw
    minecraft_pitch_degrees = direction.pitch

    to_log.update(original_minecraft_yaw_degrees=minecraft_yaw_degrees, original_minecraft_pitch_degrees=minecraft_pitch_degrees)


    # 1) convert any negative values to 0 =< degrees < 360
    if minecraft_yaw_degrees < 0:
        counterclockwise_degrees = minecraft_yaw_degrees + 180
        if counterclockwise_degrees == 0:
            minecraft_yaw_degrees = 0
        else:
            minecraft_yaw_degrees = 360 - counterclockwise_degrees
    if minecraft_pitch_degrees < 0:
        minecraft_pitch_degrees += 360
    to_log.update(adjusted_minecraft_yaw_degrees=minecraft_yaw_degrees, adjusted_minecraft_pitch_degrees=minecraft_pitch_degrees)

    # 2) adjust pitch such that the zenith = 0 degrees (and horizon = 90, down = 180)
    conventional_theta_degrees = minecraft_pitch_degrees + 90
    if conventional_theta_degrees >= 360:
        conventional_theta_degrees -= 360
    to_log.update(conventional_theta_degrees=conventional_theta_degrees)

    # 3) adjust yaw such that the north = 0 degrees (and east = 90, south = 180, west = 270)
    conventional_phi_degrees = minecraft_yaw_degrees - 180
    if conventional_phi_degrees < 0:
        conventional_phi_degrees += 360
    to_log.update(conventional_phi_degrees=conventional_phi_degrees)

    conventional_theta_radians = radians(conventional_theta_degrees)
    conventional_phi_radians = radians(conventional_phi_degrees)
    to_log.update(conventional_phi_radians=conventional_phi_radians, conventional_theta_radians=conventional_theta_radians)

    # 4) Now we can apply the conventional method of converting spherical coordinates to cartesian coordinates.
    #   see: https://en.wikipedia.org/wiki/Spherical_coordinate_system#Cartesian_coordinates
    conventional_x = radius * sin(conventional_theta_radians) * cos(conventional_phi_radians)
    conventional_y = radius * sin(conventional_theta_radians) * sin(conventional_phi_radians)
    conventional_z = radius * cos(conventional_theta_radians)
    to_log.update(conventional_x=conventional_x, conventional_y=conventional_y, conventional_z=conventional_z)

    # 5) We have calculated x, y, z relative to the middle of a sphere that adheres to ISO convention,
    #  now we need to convert back into Minecraft terms.
    #  In particular:
    #    - a conventional increase of X becomes a Minecraft decrease of Z
    #    - a conventional decrease of X becomes a Minecraft increase of Z
    #
    #    - a conventional increase of Y becomes a Minecraft increase of X
    #    - a conventional decrease of Y becomes a Minecraft decrease of X
    #
    #    - a conventional increase of Z becomes a Minecraft increase of Y
    #    - a conventional decrease of Z becomes a Minecraft decrease of Y
    minecraft_x = conventional_y
    minecraft_y = conventional_z
    minecraft_z = -1 * conventional_x
    to_log.update(minecraft_x=minecraft_x, minecraft_y=minecraft_y, minecraft_z=minecraft_z)
    log.debug("calculate_point_on_sphere: " + ', '.join("%s=%r" % (key,val) for (key,val) in sorted(to_log.iteritems())))

    return Position(minecraft_x, minecraft_y, minecraft_z)
