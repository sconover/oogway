class Position():
  def __init__(self,x,y,z):
    self.x = x
    self.y = y
    self.z = z

  def __str__(self):
    return ",".join(["x=" + str(self.x), "y=" + str(self.y), "z=" + str(self.z)])

class Direction():
  def __init__(self,yaw,pitch,roll):
    self.yaw = yaw
    self.pitch = pitch
    self.roll = roll

  def __str__(self):
    return ",".join(["yaw=" + str(self.yaw), "pitch=" + str(self.pitch), "roll=" + str(self.roll)])
