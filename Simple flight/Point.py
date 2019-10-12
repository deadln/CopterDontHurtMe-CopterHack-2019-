class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return  str(x) + ", " + str(y) + ", " + str(z)