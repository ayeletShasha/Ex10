from ship import Ship
from torpedo import Torpedo
import math
X = 'x'
Y = 'y'


class Asteroid:
    __astro_dict = {}
    """a class for 'Asteroid' objects.
     each asteroid has the following parameters:
     x_location - asteroid's location on the x axis
     y_location - asteroid's location on the y axis
     x_speed - asteroid's speed on the x axis
     y_speed - asteroid's speed on the y axis"""
    def __init__(self, x_loc=0, y_loc=0, x_speed=0,  y_speed=0, size=3):
        self.__x_location = x_loc
        self.__x_speed = x_speed
        self.__y_location = y_loc
        self.__y_speed = y_speed
        self.__size = size
        self.__radius = (self.__size*10) - 5

    def get_location(self, axis):
        """returns the asteroid's location in the requested axis"""
        if axis == X:
            return self.__x_location
        if axis == Y:
            return self.__y_location

    def get_speed(self, axis):
        """returns the asteroid's location in the requested axis"""
        if axis == X:
            return self.__x_speed
        if axis == Y:
            return self.__y_speed

    def get_size(self):
        """returns the asteroid's direction"""
        return self.__size

    def set_location(self, axis, coordinate):
        """sets the asteroid's location according to input"""
        if axis == X:
            self.__x_location = coordinate
        else:
            self.__y_location = coordinate

    def set_speed(self, axis, speed):
        """sets the asteroid's speed in a certain axis according to input"""
        if axis == X:
            self.__x_speed = speed
        else:
            self.__y_speed = speed

    def set_direction(self, direction):
        """sets the asteroid's direction according to input"""
        self.__direction = direction

    def add_to_astro_dict(self, key, obj):
        Asteroid.__astro_dict[key] = obj

    def get_radius(self):
        return self.__radius

    def has_intersection(self, obj):
        distance = math.sqrt((obj.get_location(X) -
                              self.get_location(X)) ** 2 +(obj.get_location(Y)-
                              self.get_location(Y)) ** 2)
        if distance <= obj.get_radius() + self.get_radius():
            return True
        return False
        # for ast in Asteroid.__astro_dict:
        #     distance = math.sqrt((obj.get_location(X) -
        #         Asteroid.__astro_dict[ast].get_location(X))**2 +
        #         (obj.get_location(Y) -
        #          Asteroid.__astro_dict[ast].get_location(Y))**2)
        #     if distance <= obj.get_radius() + \
        #             Asteroid.__astro_dict[ast].get_radius():
        #         return True
        # return False

