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
ALARM_TITLE = "BE CAREFUL!!"
ALARM_MSG = "YOU'VE COLLIDED WITH AN ASTEROID AND LOST A LIFE"
END_TITLE = "GAME OVER"
END_LIVES = "YOU ARE DEAD"
END_WIN = "YOU WIN!!!"
END_USER = "YOU EXIT THE GAME"

class GameRunner:

    def __init__(self, asteroids_amount = DEFAULT_ASTEROIDS_NUM):
        self.__screen = Screen()
        # define dictionaries for each object type in the game, and a list
        # of all of them
        self.__ship_dict = {}
        self.__asteroid_dict = {}
        self.__torpedo_dict = {}
        self.__dictionaries = [self.__ship_dict, self.__asteroid_dict,
                               self.__torpedo_dict]
        self.__score = 0  # Initialized score
        self.__torpedo_counter = 0
        self.__life_counter = 3

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__delta_x = self.__screen_max_x - self.__screen_min_x
        self.__delta_y = self.__screen_max_y - self.__screen_min_y

        self.create_asteroids(asteroids_amount)
        while True:
            if self.create_ship():
                break
        self.__asteroid_counter = asteroids_amount

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
        GameRunner.change_ship_heading(self, "ship")
        # iterate over all items (ship, asteroids and torpedoes)
        for dict in self.__dictionaries:
            for obj in dict:
                GameRunner.move_object(self, dict[obj])
        GameRunner.accelerate_ship(self, "ship")  # accelerates the ship
        self.draw_objects()  # re - draws all objects
        # checks collisions between all asteroids and other objects
        for ast in self.__asteroid_dict:
            if self.__asteroid_dict[ast].has_intersection(self.__ship_dict[
                                                             "ship"]):
                self.ship_collision(ast)
                break
        for ast in self.__asteroid_dict:
            for torp in self.__torpedo_dict:
                if self.__asteroid_dict[ast].has_intersection\
                            (self.__torpedo_dict[torp]):
                    self.torp_collision(ast, torp)
                    break
            break

        self.check_torpedo_lifetime()
        self.teleport_ship()

        if self.__screen.is_space_pressed():
            # check if user launched torpedo
            if len(self.__torpedo_dict) < 10: # As long as there are less
                # then 10 torpedoes in-game
                self.create_torpedo()
                self.__torpedo_counter += 1
        while True:
            if self.teleport_ship():
                break
        self.__screen.set_score(self.__score)
        self.is_game_over()

    def check_torpedo_lifetime(self):
        for torp in self.__torpedo_dict:
            if self.__torpedo_dict[torp].set_lifetime():
                self.__screen.unregister_torpedo(self.__torpedo_dict[torp])
                del self.__torpedo_dict[torp]
                break

    def torp_collision(self, ast, torp):
        ast_size = self.__asteroid_dict[ast].get_size()
        if ast_size == 3:
            self.__score += 20
            self.split_ast(ast, torp)
        elif ast_size == 2:
            self.__score += 50
            self.split_ast(ast, torp)
        elif ast_size == 1:
            self.__score += 100
            self.__screen.unregister_asteroid(self.__asteroid_dict[ast])
            self.__screen.unregister_torpedo(self.__torpedo_dict[torp])
            del self.__asteroid_dict[ast]
            del self.__torpedo_dict[torp]


    def split_ast(self, ast, torp):
        astro = self.__asteroid_dict[ast]
        torpy = self.__torpedo_dict[torp]
        new_speed_x = (torpy.get_speed(X) + astro.get_speed(X))/math.sqrt(
            astro.get_speed(X)**2 + astro.get_speed(Y)**2)
        new_speed_y = (torpy.get_speed(Y) + astro.get_speed(Y))/math.sqrt(
            astro.get_speed(X)**2 + astro.get_speed(Y)**2)
        new_size = astro.get_size() - 1
        ast_1 = Asteroid(astro.get_location(X), astro.get_location(Y), new_speed_x,
                         new_speed_y, new_size)
        ast_2 = Asteroid(astro.get_location(X), astro.get_location(Y),
                         -1*new_speed_x, -1*new_speed_y, new_size)

        self.__screen.unregister_asteroid(astro)
        self.__screen.unregister_torpedo(torpy)
        del self.__asteroid_dict[ast]
        del self.__torpedo_dict[torp]

        self.__asteroid_dict[self.__asteroid_counter + 1] = ast_1
        self.__asteroid_counter += 1
        self.__asteroid_dict[self.__asteroid_counter + 1] = ast_2
        self.__asteroid_counter += 1
        self.__screen.register_asteroid(ast_1, new_size)
        self.__screen.register_asteroid(ast_2, new_size)
        self.__screen.draw_asteroid(ast_1, ast_1.get_location(X),
                                    ast_1.get_location(Y))
        self.__screen.draw_asteroid(ast_2, ast_2.get_location(X),
                                    ast_2.get_location(Y))

    def ship_collision(self, ast):
        self.__screen.unregister_asteroid(self.__asteroid_dict[ast])
        self.__screen.show_message(ALARM_TITLE, ALARM_MSG)
        self.__screen.remove_life()
        self.__life_counter -= 1
        del self.__asteroid_dict[ast]

    def create_ship(self):
        x_coor, y_coor = self.rand_x_y()
        for ast in self.__asteroid_dict:
            if x_coor == self.__asteroid_dict[ast].get_location(X) and \
                y_coor == self.__asteroid_dict[ast].get_location(Y):
                return False

        ship = Ship(x_coor, y_coor)
        self.__ship_dict["ship"] = ship
        Screen.draw_ship(self.__screen, x_coor, y_coor, 0)
        return True

    def teleport_ship(self):
        if self.__screen.is_teleport_pressed():
            x_coor, y_coor = self.rand_x_y()
            for ast in self.__asteroid_dict:
                if x_coor == self.__asteroid_dict[ast].get_location(X) and \
                        y_coor == self.__asteroid_dict[ast].get_location(Y):
                    return False
            self.__ship_dict["ship"].set_location(X, x_coor)
            self.__ship_dict["ship"].set_location(Y, y_coor)
        return True


    def rand_x_y(self):
        x_coor = randint(self.__screen_min_x, self.__screen_max_x)
        y_coor = randint(self.__screen_min_y, self.__screen_max_y)
        return x_coor, y_coor

    def create_asteroids(self, asteroids_amount):
        for i in range(asteroids_amount):
            ast_x_coor = randint(self.__screen_min_x, self.__screen_max_x)
            ast_y_coor = randint(self.__screen_min_y, self.__screen_max_y)
            speed_x = randint(1, 4)
            speed_y = randint(1, 4)
            ast = Asteroid(ast_x_coor, ast_y_coor, speed_x, speed_y)
            self.__screen.register_asteroid(ast, 3)
            self.__screen.draw_asteroid(ast, ast_x_coor, ast_y_coor)
            self.__asteroid_dict[i] = ast
            # asteroids are represented as numbers in the object dictionary
            # Asteroid.add_to_astro_dict(Asteroid, i, ast)

    def move_object(self, object):
        """This method moves a given object by a formula defined in the API.
        It does this for both x and y axis"""
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

    def draw_objects(self):
        # draw ship
        self.__screen.draw_ship(self.__ship_dict["ship"].get_location(X),
                                self.__ship_dict["ship"].get_location(Y),
                                self.__ship_dict["ship"].get_heading())
        for ast in self.__asteroid_dict:
            self.__screen.draw_asteroid(self.__asteroid_dict[ast],
                                        self.__asteroid_dict[ast].get_location(
                                            X),
                                        self.__asteroid_dict[ast].get_location(
                                            Y))
        for torp in self.__torpedo_dict:
            self.__screen.draw_torpedo(self.__torpedo_dict[torp],
                                       self.__torpedo_dict[
                                           torp].get_location(X),
                                       self.__torpedo_dict[torp].get_location(
                                           Y), self.__torpedo_dict[
                                           torp].get_heading())

    def change_ship_heading(self, ship):
        """This function changes the ships heading if user presses left or
        right accordingly
        :param ship: A STRING"""

        ship = self.__ship_dict[ship]
        ship_dir = ship.get_heading()
        if self.__screen.is_left_pressed():
            ship.set_heading(ship_dir + 7)
        elif self.__screen.is_right_pressed():
            ship.set_heading(ship_dir - 7)
        return

    def accelerate_ship(self, ship):
        """This method accelerates the ship when 'up' key is pressed."""
        if self.__screen.is_up_pressed():
            ship = self.__ship_dict[ship]
            cur_x_speed = ship.get_speed(X)
            cur_y_speed = ship.get_speed(Y)
            cur_heading = ship.get_heading()
            new_x_speed = cur_x_speed + math.cos(math.radians(cur_heading))
            new_y_speed = cur_y_speed + math.sin(math.radians(cur_heading))
            ship.set_speed(X, new_x_speed)
            ship.set_speed(Y, new_y_speed)
        return

    def create_torpedo(self):
        torp = Torpedo(self.__ship_dict["ship"].get_location(X),
                       self.__ship_dict["ship"].get_location(Y),
                       self.__ship_dict["ship"].get_speed(X),
                       self.__ship_dict["ship"].get_speed(Y),
                       self.__ship_dict["ship"].get_heading())
        self.__screen.register_torpedo(torp)
        self.__screen.draw_torpedo(torp, torp.get_location(X),
                                   torp.get_location(
            Y), torp.get_heading())
        self.__torpedo_dict[self.__torpedo_counter] = torp

    def is_game_over(self):
        if self.__life_counter == 0:
            self.__screen.show_message(END_TITLE, END_LIVES)
        elif len(self.__asteroid_dict) == 0:
            self.__screen.show_message(END_TITLE, END_WIN)
        elif self.__screen.should_end():
            self.__screen.show_message(END_TITLE, END_USER)
        else:
            return
        self.__screen.end_game()


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
