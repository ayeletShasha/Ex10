
class Ship:

    def __init__(self, x_loc=0, y_loc=0, x_speed=0,  y_speed=0, dir=0):
        self.x_location = x_loc
        self.x_speed = x_speed
        self.y_location = y_loc
        self.y_speed = y_speed
        self.direction = dir

    def set_location(self, axis, coordinate):
        if axis == "x":
            self.x_location = coordinate
        else:
            self.y_location = coordinate

    def set_speed(self, axis, speed):
        if axis == "x":
            self.x_speed = speed
        else:
            self.y_speed = speed

    def set_direction(self, direction):
        self.direction = direction
