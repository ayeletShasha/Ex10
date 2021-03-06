X = 'x'
Y = 'y'


class Ship:
    """a class for 'Ship' objects.
     each asteroid has the following parameters:
     x_location - asteroid's location on the x axis
     y_location - asteroid's location on the y axis
     x_speed - asteroid's speed on the x axis
     y_speed - asteroid's speed on the y axis"""
    def __init__(self, x_loc=0, y_loc=0, x_speed=0,  y_speed=0, heading=0):
        self.__x_location = x_loc
        self.__x_speed = x_speed
        self.__y_location = y_loc
        self.__y_speed = y_speed
        self.__heading = heading
        self.__radius = 1

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

    def get_heading(self):
        """returns the asteroid's direction"""
        return self.__heading

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

    def set_heading(self, heading):
        """sets the asteroid's direction according to input"""
        self.__heading = heading

    def get_radius(self):
        return self.__radius