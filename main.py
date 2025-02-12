# TODO:
# Gameover screen when the player collides into a monster.
# Add option to replay game after clearing.

import pygame as pg
from random import randint
from datetime import timedelta
import sys

class RainingCoins:
    def __init__(self):
        self.__initialize_game()
        self.__initialize_assets()

    def __initialize_game(self):
        pg.init()
        pg.display.set_caption("RainingCoins")
        self.__game_font = pg.font.SysFont("Arial", 24)
        self.__game_clear = False
        self.__game_over = False
        self.__screen = Screen()
        self.__time = Time(self)
        self.__clock = pg.time.Clock()

    @property
    def game_font(self):
        return self.__game_font

    @property
    def game_clear(self):
        return self.__game_clear
    
    @property
    def game_over(self):
        return self.__game_over

    @property
    def screen(self):
        return self.__screen

    @property
    def time(self):
        return self.__time

    def __initialize_assets(self):
        robot = pg.image.load("robot.png")
        self.__robot = Robot(self, robot)

        coin = pg.image.load("coin.png")
        self.__coin = Coin(self, coin)
        new_size = (coin.get_size()[0] // 2, coin.get_size()[1] // 2)
        self.__coin_icon = pg.transform.scale(coin, new_size)

        monster = pg.image.load("monster.png")
        self.__monster = Monster(self, monster)
        new_size = (monster.get_size()[0] // 2, monster.get_size()[1] // 2)
        self.__monster_icon = pg.transform.scale(monster, new_size)

    @property
    def robot(self):
        return self.__robot
    
    @property
    def coin(self):
        return self.__coin
    
    @property
    def monster(self):
        return self.__monster

    def play_game(self):
        test = False
        while not test:
            self.__check_events()
            self.__draw_screen()
        while test:
            self.__check_events()
            self.__draw_screen_test()

    def __check_events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    sys.exit()
                self.__robot.key_pressed[event.key] = True
            if event.type == pg.KEYUP:
                del self.__robot.key_pressed[event.key]
            if event.type == pg.QUIT:
                exit()

    def __draw_screen(self):
        self.__screen.clear_screen()
        self.__robot.draw()
        
        self.__coin.draw()
        self.__monster.draw()
        self.__draw_ui()

        self.__clock.tick(60)
        pg.display.flip()   

    def __draw_ui(self):
        self.__time.draw_time()

        if self.__is_game_clear():
            self.__draw_game_clear()

        self.draw_text("Esc = exit game", 20, 440)
        pg.draw.line(self.__screen.screen, (255, 0, 0), (0, 430), (self.__screen.width, 430), 3)

        self.draw_text(f"x{self.__coin.count}", 520, 440)
        self.__screen.render_screen(self.__coin_icon, 490, 445)

        self.draw_text(f"x{self.__monster.count}", 430, 440)
        self.__screen.render_screen(self.__monster_icon, 400, 435)

    def draw_text(self, hud: str, x: int, y: int):
        self.__screen.render_screen(self.__game_text(hud, self.__game_font), x, y)

    def __game_text(self, hud: str, font: pg.font):
        return font.render(hud, True, (255, 0, 0))

    def __draw_game_clear(self):
        clear_font = pg.font.SysFont("Arial", 69)
        win_text = self.__game_text("You win!", clear_font)

        center_x = self.__screen.width / 2 - win_text.get_size()[0] / 2
        center_y = self.__screen.height / 2 - win_text.get_size()[1] / 2

        self.__screen.render_screen(win_text, center_x, center_y)
        self.__game_clear = True

    def __is_game_clear(self):
        return self.__time.is_time_up()

    def __draw_screen_test(self):
        self.__screen.clear_screen()
        self.__draw_ui()
        self.__screen.render_screen(self.__monster_icon, 400, 435)
        pg.display.flip()

class Screen:
    def __init__(self):
        self.__width = 640
        self.__height = 480
        self.__screen = pg.display.set_mode((self.__width, self.__height))

    @property
    def width(self):
        return self.__width
    
    @property
    def height(self):
        return self.__height
    
    @property
    def screen(self):
        return self.__screen
    
    def clear_screen(self):
        self.__screen.fill((40, 40, 40))

    def render_screen(self, image: pg.image, x: int, y: int):
        self.__screen.blit(image, (x, y))

class Time:
    def __init__(self, game_instance: RainingCoins):
        self.__game_instance = game_instance
        self.__timer = timedelta(minutes = 2)
        self.__start_ticks = pg.time.get_ticks() # measured in milliseconds 
        self.__time_up = False        

    def is_time_up(self):
        return self.__time_up

    def draw_time(self):
        minutes, seconds = self.__calculate_time_remaining()
        self.__game_instance.draw_text(f"{minutes}:{seconds:02}", 580, 440)

    def __calculate_time_remaining(self):
        current_ticks = pg.time.get_ticks()
        elapsed_seconds = (current_ticks - self.__start_ticks) // 1000
        time_remaining = self.__timer - timedelta(seconds = elapsed_seconds)

        total_seconds = int(time_remaining.total_seconds())

        if total_seconds <= 0:
            self.__time_up = True
            return (0, 0)

        return divmod(total_seconds, 60)

class DrawObject:
    def __init__(self, game_instance: RainingCoins):
        self._game_instance = game_instance

    def draw(self):
        self._render_object()
        if self._game_instance.time.is_time_up():
            return
        self._update_object_xy()

    def _render_object(self):
        pass

    def _update_object_xy(self):
        pass

class Robot(DrawObject):
    def __init__(self, game_instance: RainingCoins, robot: pg.image):
        super().__init__(game_instance)
        self.__robot = robot
        self.__speed = 5
        self.__controls = []
        self.__controls.append((pg.K_LEFT, -self.__speed, 0))
        self.__controls.append((pg.K_RIGHT, self.__speed, 0))
        self.__key_pressed = {}

        # a height of 430 will be used for the ground
        self.__robot_x = 0
        self.__robot_y = 430 - self.__robot.get_height()

    @property
    def key_pressed(self):
        return self.__key_pressed

    def _render_object(self):
        self._game_instance.screen.render_screen(self.__robot, self.__robot_x, self.__robot_y)

    def _update_object_xy(self):
        for key in self.__controls:
            if key[0] in self.__key_pressed:
                self.__robot_x += key[1]
                self.__robot_y += key[2]

        self.__robot_x = min(self.__robot_x, self._game_instance.screen.width - self.__robot.get_width())
        self.__robot_x = max(self.__robot_x, 0)        

    def get_coordinates(self):
        return (self.__robot_x, self.__robot_y)
    
    def get_width(self):
        return self.__robot.get_width()

class RainingItem(DrawObject):
    def __init__(self, game_instance: RainingCoins, image: pg.image):
        super().__init__(game_instance)
        self._image = image
        self._count = 0
        self._frequency = 20
        self._speed = 2
        self._positions = self._start_positions()

    def _start_positions(self):
        return [[-9001, self._game_instance.screen.height] for i in range(self._frequency)]

    def _render_object(self):
        for i in range(self._frequency):
            self._game_instance.screen.render_screen(self._image, self._positions[i][0], self._positions[i][1])

    def _update_object_xy(self):
        for i in range(self._frequency):
            current_item = self._positions[i]
            if self.__detect_collision(self._game_instance.robot, i):
                self._collide_condition(i)
            self._monster_count(i)
            if current_item[1] < 430 - self.image_height():
                current_item[1] += self._speed
            else:
                self._floor_boundary(current_item, i)

    def _randomize_pos(self):
        return [randint(0, self._game_instance.screen.width - self.image_width()), -randint(100, 1000)]

    # Hook Method
    def _collide_condition(self):
        pass

    # Hook Method
    def _monster_count(self, i: int):
        pass

    # Hook Method
    def _floor_boundary(self, current_item: list[int], index: int):
        pass

    def __detect_collision(self, robot: Robot, item_index: int):
        robot_xy = robot.get_coordinates()
        if self._positions[item_index][1] + self._image.get_height() >= robot_xy[1]:
            item_half_width = self._image.get_width() / 2
            robot_half_width = robot.get_width() / 2
            item_middle = self._positions[item_index][0] + item_half_width
            robot_middle = robot_xy[0] + robot_half_width
            return abs(item_middle - robot_middle) <= item_half_width + robot_half_width
        return False
    
    def image_height(self):
        return self._image.get_height()
    
    def image_width(self):
        return self._image.get_width()
    
    @property
    def count(self):
        return self._count

    def set_frequency(self, frequency: int):
        self._frequency = frequency
    
    def set_speed(self, speed: int):
        self._speed = speed

class Coin(RainingItem):
    def __init__(self, game_instance: RainingCoins, coin: pg.image):
        super().__init__(game_instance, coin)

    def _start_positions(self):
        return [self._randomize_pos() for i in range(self._frequency)]

    def _collide_condition(self, i: int):
        self._positions[i][0], self._positions[i][1] = self._randomize_pos()
        self._count += 1

class Monster(RainingItem):
    def __init__(self, game_instance: RainingCoins, monster: pg.image):
        super().__init__(game_instance, monster)
        self.__visited = [False] * self._frequency

    def _collide_condition(self, i: int):
        sys.exit()

    def _monster_count(self, i: int):
        if (not self.__visited[i] and self._positions[i][1] >= 0 and \
        self._positions[i][1] + self._image.get_height() <= self._game_instance.screen.height):
            self._count += 1
            self.__visited[i] = True

    def _floor_boundary(self, current_monster: list[int], i: int):
        current_monster[0], current_monster[1] = self._randomize_pos()
        self.__visited[i] = False

###########################################################################################################################

if __name__ == "__main__":
    rc = RainingCoins()
    rc.monster.set_frequency(8)
    rc.play_game()
