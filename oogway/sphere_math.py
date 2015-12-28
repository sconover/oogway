from math import sin, cos, radians, tan
from orientation import Position
from logging import getLogger

def calculate_point_on_sphere2(direction, radius):
    log = getLogger(__name__)
    to_log = {}

    minecraft_yaw_degrees = direction.yaw
    minecraft_pitch_degrees = direction.pitch

    to_log.update(original_minecraft_yaw_degrees=minecraft_yaw_degrees, original_minecraft_pitch_degrees=minecraft_pitch_degrees)

    # In Minecraft:
    #   Yaw 180 (or -180) degrees is Due North
    #   Moving North decreases Z (+N = -z)
    #
    #   Yaw -90 degrees is Due East
    #   Moving East increases X (+E = +x)
    #
    #   Yaw 0 degrees is Due South
    #   Moving South increases Z (+S = +z)
    #
    #   Yaw +90 degrees is Due West
    #   Moving West decreases X (+W = -x)
    #
    #   Pitch 0 degrees is the horizon
    #
    #   Pitch -90 degrees is straight up (zenith)
    #   Moving up increases Y (+U = +y)
    #
    #   Pitch +90 degrees is straight down
    #   Moving down decreases Y (+D = -y)


    # From https://en.wikipedia.org/wiki/Spherical_coordinate_system#Conventions
    # "The use of (r, theta, phi) to denote radial distance, inclination (or elevation), and azimuth, respectively, 
    #  is common practice in physics, and is specified by ISO standard 80000-2 :2009, and earlier in ISO 31-11 (1992)."
    #
    # So, according to the ISO standard:
    # pitch = inclination/elevation/altitude = theta
    # yaw = azimuth = phi
    #
    # We shall map minecraft values to the following, such that we can employ conventional
    # methods of calculating cartesian coordinates from sperical coordinates.
    #
    # Roughly, we are going to:
    #   - "tilt" the ptich such that the zenith is zero degrees
    #   - adjust degrees such that 0 =< degrees < 360
    #
    #   Yaw/Phi 0 shall be Due North
    #   Moving North increases X (+N = +x)
    #
    #   Yaw/Phi 90 degrees is Due East
    #   Moving East increases Y (+E = +y)
    #
    #   Yaw/Phi 180 degrees is Due South
    #   Moving South decreases X (+S = -x)
    #
    #   Yaw/Phi 270 degrees is Due West
    #   Moving West decreases Y (+W = -y)
    #
    #   Pitch/Theta 0 degrees is the zenith
    #   Moving up increases Z (+U = +z)
    #
    #   Pitch/Theta 90 degrees is the horizon
    #
    #   Pitch/Theta 180 degrees is straight down
    #   Moving down decreases Z (+D = -z)


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
    log.debug("calculate_point_on_sphere: " + ', '.join("%s=%r" % (key,val) for (key,val) in to_log.iteritems()))

    return Position(minecraft_x, minecraft_y, minecraft_z)



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

    In the international convention:
      - The Z axis points "up-down". Imagine
        the earth: the Z axis would pass through the poles, and Z = 0 degrees
        would be the North Pole, and Z=180 degrees would be the South Pole.
      - X and Y axes can be imagined as being in the plane of the Equator.
      - the Prime Meridian (and its antimeridian) is the XZ plane - IRL this runs through Greenwich, England.
      - see also https://en.wikipedia.org/wiki/Axes_conventions
        - especially: https://en.wikipedia.org/wiki/Axes_conventions#/media/File:ECEF_ENU_Longitude_Latitude_relationships.svg

    In Minecraft:
      - The Y axis points "up-down".
      - Y = 0 degrees is in the direction of the horizon
      - see this thread for more details:
        https://bukkit.org/threads/tutorial-how-to-calculate-vectors.138849/
    """

    # yaw = direction.yaw - 90
    # if yaw < 0:
    #     yaw += 360

    # pitch = direction.pitch + 90
    # if pitch >= 360:
    #     pitch -= 360



    print "======== direction: yaw=" + str(direction.yaw) + " pitch=" + str(direction.pitch)

    theta_degrees = direction.yaw
    phi_degrees = direction.pitch

    theta = radians(theta_degrees)
    phi = radians(phi_degrees)

    # print theta
    # print phi

    convention_x = radius * sin(theta) * cos(phi)
    convention_y = radius * sin(theta) * sin(phi)
    convention_z = radius * cos(theta)

    minecraft_x = convention_y
    minecraft_y = convention_z
    minecraft_z = -1 * convention_x

    # print convention_x

    print (minecraft_x, minecraft_y, minecraft_z)

    # print direction

    yaw = direction.yaw - 90
    if yaw < 0:
        yaw += 360

    pitch = direction.pitch + 90
    if pitch >= 360:
        pitch -= 360

    # yaw is the angle around the z axis, aka phi
    yaw_radians = radians(yaw)

    # pitch is the angle around the y axis, aka theta
    pitch_radians = radians(pitch)

    # print yaw_radians
    # print pitch_radians

    minecraft_x = radius * -1 * cos(pitch_radians) * sin(yaw_radians)
    minecraft_y = radius * sin(pitch_radians)
    minecraft_z = radius * cos(pitch_radians) * cos(yaw_radians)

    # print minecraft_x

    print (minecraft_x, minecraft_y, minecraft_z)

    # TODO: unit test this
    #   ...or just use unit_test.py

    # classical convention
    # z is up-down
    # y n-s
    # x e-w
    #
    # think looking down on the north pole
    # max z = north pole
    #   z is 0 at the equator
    #   np is +90
    #   sp is 270 (or -90)

    # wikipedia
    # origin z = north pole
    #   z is 90 at the equator
    #   z is 180 at the equator
    #   np is +90
    #   sp is 270 (or -90)

    # geographical reference...
    # yaw, pitch are centered on the equator


    #
    # x = 0 is greenwich
    #   x = 90 at ny
    #

    # wikipedia:
    #


    # from link above:
    # "The "+ 90" adds 90 degrees to the players pitch/yaw which corrects
    # for the 90 degree rotation Notch added."


    # print "yaw_radians=" + str(yaw_radians) + " pitch_radians=" + str(pitch_radians)

    # print "sin(pitch_radians)=" + str(sin(pitch_radians)) + \
    #  "cos(yaw_radians)=" + str(cos(yaw_radians))
    # x = radius * sin(pitch_radians) * cos(yaw_radians)
    # y = radius * sin(pitch_radians) * sin(yaw_radians)
    # z = radius * cos(pitch_radians)

    # y = radius * sin(pitch_radians)
    # x = radius * cos(pitch_radians) * sin(yaw_radians)
    # z = radius * cos(yaw_radians)


    # print "cos(pitch_radians)=" + str(cos(pitch_radians)) + " sin(yaw_radians)=" + str(sin(yaw_radians))
    # print "sin(pitch_radians)=" + str(sin(pitch_radians))
    # print "cos(pitch_radians)=" + str(cos(pitch_radians)) + " cos(yaw_radians)=" + str(cos(yaw_radians))

    # x = radius * -1 * cos(pitch_radians) * sin(yaw_radians)
    # y = radius * sin(pitch_radians)
    # z = radius * cos(pitch_radians) * cos(yaw_radians)


    # x = radius * sin(theta) * cos(phi)
    # y = radius * sin(theta) * sin(phi)
    # z = radius * cos(theta)

    parts = [
        ["x", minecraft_x],
        ["y", minecraft_y],
        ["z", minecraft_z],
        ["yaw", direction.yaw],
        ["theta", theta],
        ["pitch", direction.pitch],
        ["phi", phi],
        ["sin(theta)", sin(theta)],
        ["cos(phi)", cos(phi)],
        ["sin(theta)", sin(theta)],
        ["sin(phi)", sin(phi)],
        ["cos(theta)", cos(theta)]]

    # print " ".join(map(lambda (k,v): k + "=" + str(round(v,4)).ljust(6), parts))

    return Position(minecraft_x, minecraft_y, minecraft_z)


    # public static Vector3d createDirectionRad(double theta, double phi) {
    #     final double f = TrigMath.sin(phi);
    #     return new Vector3d(f * TrigMath.cos(theta), f * TrigMath.sin(theta), TrigMath.cos(phi));
    # }


    # public Vector getDirection() {
    #     Vector vector = new Vector();

    #     double rotX = this.getYaw();
    #     double rotY = this.getPitch();

    #     vector.setY(-Math.sin(Math.toRadians(rotY)));

    #     double xz = Math.cos(Math.toRadians(rotY));

    #     vector.setX(-xz * Math.sin(Math.toRadians(rotX)));
    #     vector.setZ(xz * Math.cos(Math.toRadians(rotX)));

    #     return vector;
    # }

# /**
#      * Sets the {@link #getYaw() yaw} and {@link #getPitch() pitch} to point
#      * in the direction of the vector.
#      */
#     public Location setDirection(Vector vector) {
#         /*
#          * Sin = Opp / Hyp
#          * Cos = Adj / Hyp
#          * Tan = Opp / Adj
#          *
#          * x = -Opp
#          * z = Adj
#          */
#         final double _2PI = 2 * Math.PI;
#         final double x = vector.getX();
#         final double z = vector.getZ();

#         if (x == 0 && z == 0) {
#             pitch = vector.getY() > 0 ? -90 : 90;
#             return this;
#         }

#         double theta = Math.atan2(-x, z);
#         yaw = (float) Math.toDegrees((theta + _2PI) % _2PI);

#         double x2 = NumberConversions.square(x);
#         double z2 = NumberConversions.square(z);
#         double xz = Math.sqrt(x2 + z2);
#         pitch = (float) Math.toDegrees(Math.atan(-vector.getY() / xz));

#         return this;
#     }
