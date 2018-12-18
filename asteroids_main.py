from screen import Screen
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
from random import randint
import math
import sys

DEFAULT_ASTEROIDS_NUM = 5
X = "x"
Y = "y"

class GameRunner:

    def __init__(self, asteroids_amount):
        self.__screen = Screen()

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__delta_x = self.__screen_max_x - self.__screen_min_x
        self.__delta_y = self.__screen_max_y - self.__screen_min_y

        x_coor = randint(self.__screen_min_x, self.__screen_max_x)
        y_coor = randint(self.__screen_min_y, self.__screen_max_y)
        self.__object_dict = {}

        ship = Ship(x_coor, y_coor)
        self.__object_dict["ship"] = ship
        Screen.draw_ship(self.__screen, x_coor, y_coor, 0)


    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        # Your code goes here
        GameRunner.change_ship_direction(self, "ship")
        GameRunner.move_object(self, "ship")
        GameRunner.accelerate_ship(self, "ship")

    def move_object(self, object):
        """This method moves a given object by a formula defined in the API.
        It does this for both x and y axis"""
        object = self.__object_dict[object]
        x_speed = object.get_speed(X)
        y_speed = object.get_speed(Y)
        x_coord = object.get_location(X)
        y_coord = object.get_location(Y)

        new_x_coord = ((x_speed + x_coord - self.__screen_min_x)
                       % self.__delta_x) + self.__screen_min_x
        new_y_coord = ((y_speed + y_coord - self.__screen_min_y)
                       % self.__delta_y) + self.__screen_min_y
        object.set_location(X, new_x_coord)
        object.set_location(Y, new_y_coord)

    def change_ship_direction(self, ship):
        """This function changes the ships direction if user presses left or
        right accordingly
        :param ship: A STRING"""

        ship = self.__object_dict[ship]
        ship_dir = ship.get_direction()
        if self.__screen.is_left_pressed():
            ship.set_direction(ship_dir + 7)
        elif self.__screen.is_right_pressed():
            ship.set_direction(ship_dir - 7)
        return

    def accelerate_ship(self, ship):
        if self.__screen.is_up_pressed():
            ship = self.__object_dict[ship]
            cur_x_speed = ship.get_speed(X)
            cur_y_speed = ship.get_speed(Y)
            cur_heading = ship.get_direction()
            new_x_speed = cur_x_speed + math.cos(math.radians(cur_heading))
            new_y_speed = cur_y_speed + math.sin(math.radians(cur_heading))
            ship.set_speed(X, new_x_speed)
            ship.set_speed(Y, new_y_speed)
        return

def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
