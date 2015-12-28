class Position():
    def __init__(self,x,y,z):
        self.x = round(x, 3)
        self.y = round(y, 3)
        self.z = round(z, 3)

    def is_possible_in_a_minecraft_world(self):
        return self.x <= 29999999 and self.x >= -29999999 and \
            self.y <= 255 and self.y >= 0 and \
            self.z <= 29999999 and self.z >= -29999999

    def __str__(self):
        return ",".join(["x=" + str(self.x), "y=" + str(self.y), "z=" + str(self.z)])

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and abs(self.x - other.x) < 0.0001
            and abs(self.y - other.y) < 0.0001
            and abs(self.z - other.z) < 0.0001)

class Direction():
    def __init__(self,yaw,pitch,roll):
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll

    def __str__(self):
        return ",".join(["yaw=" + str(self.yaw), "pitch=" + str(self.pitch), "roll=" + str(self.roll)])
