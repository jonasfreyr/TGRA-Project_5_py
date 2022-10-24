import math
from math import sqrt

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __str__(self):
        return f"P({self.x}, {self.y}, {self.z})"

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    def __len__(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def __str__(self):
        return f"V(x: {self.x}, y: {self.y}, z: {self.z})"

    def copy(self):
        return Vector(self.x, self.y, self.z)

    def length2D(self):
        return sqrt(self.x * self.x + self.z * self.z)

    def rotate2dXAxis(self, angle):
        rad = math.radians(angle)

        cs = math.cos(rad)
        sn = math.sin(rad)

        py = self.y * cs - self.z * sn
        pz = self.y * sn + self.z * cs

        self.y = py
        self.z = pz

    def rotate2d(self, angle):
        rad = math.radians(angle)

        cs = math.cos(rad)
        sn = math.sin(rad)

        px = self.x * cs - self.z * sn
        pz = self.x * sn + self.z * cs

        self.x = px
        self.z = pz

    def normalize2D(self):
        length = self.length2D()
        self.x /= length
        self.z /= length

    def normalize(self):
        length = self.__len__()
        self.x /= length
        self.y /= length
        self.z /= length

    def set(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def to_array(self):
        return self.x, self.y, self.z

    def cross(self, other):
        return Vector(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)


def lerp(v1: Vector, v2: Vector, t: float) -> Vector:
    temp_1 = v1 * (1 - t)
    temp_2 = v2 * t

    return temp_1 + temp_2


if __name__ == '__main__':
    t = 0.75
    P1 = Vector(15, 5, 2)
    P2 = Vector(10, 2, 2)
    P3 = Vector(5, 7, 2)
    P4 = Vector(0, 0, 2)

    P12 = lerp(P1, P2, t)
    P23 = lerp(P2, P3, t)
    P34 = lerp(P3, P4, t)

    print("P12:", P12)
    print("P23:", P23)
    print("P34:", P34)

    P1223 = lerp(P12, P23, t)
    P2334 = lerp(P23, P34, t)

    print("P1223:", P1223)
    print("P2334:", P2334)

    Final = lerp(P1223, P2334, t)

    print("Final:", Final)