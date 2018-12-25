import math
X = 'x'
Y = 'y'


class Torpedo:
    """a class for 'Torpedo' objects.
     each torpedo has the following parameters:
     x_location - torpedo's location on the x axis
     y_location - torpedo's location on the y axis
     x_speed - torpedo's speed on the x axis
     y_speed - torpedo's speed on the y axis"""
    def __init__(self, x_loc=0, y_loc=0, x_speed=0,  y_speed=0, heading=0,
                 radius=4):
        self.__x_location = x_loc
        self.__x_speed = x_speed + (2*math.cos(math.radians(heading)))
        self.__y_location = y_loc
        self.__y_speed = y_speed + (2*math.sin(math.radians(heading)))
        self.__heading = heading
        self.__radius = radius
        self.__lifetime = 0

    def get_location(self, axis):
        """returns the torpedo's location in the requested axis"""
        if axis == X:
            return self.__x_location
        if axis == Y:
            return self.__y_location

    def get_speed(self, axis):
        """returns the torpedo's location in the requested axis"""
        if axis == X:
            return self.__x_speed
        if axis == Y:
            return self.__y_speed

    def get_heading(self):
        """returns the torpedo's heading"""
        return self.__heading

    def set_location(self, axis, coordinate):
        """sets the torpedo's location according to input"""
        if axis == X:
            self.__x_location = coordinate
        else:
            self.__y_location = coordinate

    def set_speed(self, axis, speed):
        """sets the torpedo's speed in a certain axis according to input"""
        if axis == X:
            self.__x_speed = speed
        else:
            self.__y_speed = speed

    def set_heading(self, heading):
        """sets the torpedo's heading according to input"""
        self.__heading = heading

    def get_radius(self):
        """returns the torpedo's radius"""
        return self.__radius

    def set_lifetime(self):
        """sets the torpedo's lifetime. returns True if lifetime has reached
        200, None if it has reached 150, and False if it hasn't reached any
        of these benchmarks"""
        self.__lifetime += 1
        if self.__lifetime == 200:
            return True
        elif self.__lifetime == 150:
            return None
        return False
