from screen import Screen
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
from random import randint
import sys

DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:

    def __init__(self, asteroids_amount):
        self.__screen = Screen()

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__delta_x = self.__screen_max_x - self.__screen_min_x
        self.__delta_y = self.__screen_max_y - self.__screen_min_y

        x = randint(self.__screen_min_x, self.__screen_max_x)
        y = randint(self.__screen_min_y, self.__screen_max_y)
        self.object_dict = {}

        ship = Ship(x, y)
        self.object_dict["ship"] = ship
        Screen.draw_ship(self.__screen, x, y, 0)


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
        pass

    def move_object(self, object):
        """This method moves a given object by a formula defined in the API.
        It does this for both x and y axis"""
        object = self.object_dict[object]
        x_speed = object.x_speed
        y_speed = object.y_speed
        x_coord = object.x_location
        y_coord = object.y_location

        new_x_coord = ((x_speed + x_coord - self.__screen_min_x)
                       % self.__delta_x) + self.__screen_min_x
        new_y_coord = ((y_speed + y_coord - self.__screen_min_y)
                       % self.__delta_y) + self.__screen_min_y
        return new_x_coord, new_y_coord

    def change_ship_direction(self, ship):
        """This function changes the ships direction if user presses left or
        right accordingly"""
        ship = self.object_dict[ship]
        ship_dir = ship.get_direction()
        if Screen.is_left_pressed():
            ship.set_direction(ship_dir + 7)
        elif Screen.is_right_pressed():
            ship.set_direction(ship_dir - 7)
        return


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
