from math import sin, cos, radians, tan
from orientation import Position

# note: https://bukkit.org/threads/tutorial-how-to-calculate-vectors.138849/

def calculate_point_on_sphere(direction, radius):

    # from link above:
    # "The "+ 90" adds 90 degrees to the players pitch/yaw which corrects
    # for the 90 degree rotation Notch added."

    # yaw is the angle around the z axis, aka phi
    yaw_radians = radians(direction.yaw)

    # pitch is the angle around the y axis, aka theta
    pitch_radians = radians(direction.pitch)



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

    x = radius * -1 * cos(pitch_radians) * sin(yaw_radians)
    y = radius * -1 * sin(pitch_radians)
    z = radius * cos(pitch_radians) * cos(yaw_radians)

    parts = [
        ["x", x],
        ["y", y],
        ["z", z],
        ["yaw", direction.yaw],
        ["yr", yaw_radians],
        ["pitch", direction.pitch],
        ["pr", pitch_radians],
        ["cos(pr)", cos(pitch_radians)],
        ["sin(yr)", sin(yaw_radians)],
        ["sin(pr)", sin(pitch_radians)],
        ["cos(yr)", cos(yaw_radians)]]

    # print " ".join(map(lambda (k,v): k + "=" + str(round(v,4)).ljust(6), parts))

    return Position(x, y, z)


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
