# TODO:
# Gameover screen when the player collides into a monster.
# Game Clear screen when the time runs out
# Update the coin count when player collides into a coin.

import pygame as pg
from random import randint
from datetime import datetime, timedelta
import sys

class RainingCoins:
    def __init__(self):
        self.initialize_game()
        self.initialize_assets()

    def initialize_game(self):
        pg.init()
        pg.display.set_caption("Raining Coins")
        self.game_font = pg.font.SysFont("Arial", 24)
        self.width = 640
        self.height = 480
        self.screen = pg.display.set_mode((self.width, self.height))
        self.timer = timedelta(minutes = 2)
        self.start_ticks = pg.time.get_ticks() # measured in milliseconds         
        self.clock = pg.time.Clock()

    def initialize_assets(self):
        robot = pg.image.load("robot.png")
        self.robot = Robot(self, robot)

        coin = pg.image.load("coin.png")
        self.coin = Coin(self, coin)
        new_size = (coin.get_size()[0] // 2, coin.get_size()[1] // 2)
        self.coin_icon = pg.transform.scale(coin, new_size)

        monster = pg.image.load("monster.png")
        self.monster = Monster(self, monster)
        new_size = (monster.get_size()[0] // 2, monster.get_size()[1] // 2)
        self.monster_icon = pg.transform.scale(monster, new_size)

    def play_game(self):
        test = False
        while not test:
            self.check_events()
            self.draw_screen()
        while test:
            self.check_events()
            self.draw_screen_test()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    sys.exit()
                self.robot.key_pressed[event.key] = True
            if event.type == pg.KEYUP:
                del self.robot.key_pressed[event.key]
            if event.type == pg.QUIT:
                exit()

    def draw_screen(self):
        self.screen.fill((40,40,40))
        self.__draw_ui()
        self.robot.draw()
        
        self.coin.draw()
        self.monster.draw()

        self.clock.tick(60)
        pg.display.flip()   

    def __draw_ui(self):
        current_ticks = pg.time.get_ticks()
        elapsed_seconds = (current_ticks - self.start_ticks) // 1000
        time_remaining = self.timer - timedelta(seconds = elapsed_seconds)

        total_seconds = int(time_remaining.total_seconds())
        minutes, seconds = divmod(total_seconds, 60)

        game_text = self.game_font.render(f"{minutes}:{seconds:02}", True, (255, 0, 0))
        self.screen.blit(game_text, (580, 440))

        game_text = self.game_font.render("Esc = exit game", True, (255, 0, 0))
        self.screen.blit(game_text, (20, 440))
        pg.draw.line(self.screen, (255, 0, 0), (0, 430), (self.width, 430), 3)

        game_text = self.game_font.render(f"x{self.coin.count}", True, (255, 0, 0))
        self.screen.blit(self.coin_icon, (490, 445))
        self.screen.blit(game_text, (520, 440))

        game_text = self.game_font.render(f"x{self.monster.count}", True, (255, 0, 0))
        self.screen.blit(self.monster_icon, (400, 435))
        self.screen.blit(game_text, (430, 440))

    def draw_screen_test(self):
        self.screen.fill((40, 40, 40))
        self.__draw_ui()
        self.screen.blit(self.monster_icon, (400, 435))
        pg.display.flip()

class Robot:
    def __init__(self, game_instance: RainingCoins, robot: pg.image):
        self.game_instance = game_instance
        self.robot = robot
        self.speed = 5
        self.controls = []
        self.controls.append((pg.K_LEFT, -self.speed, 0))
        self.controls.append((pg.K_RIGHT, self.speed, 0))
        self.key_pressed = {}

        # a height of 430 will be used for the ground
        self.robot_x = 0
        self.robot_y = 430 - self.robot.get_height()

    def draw(self):
        for key in self.controls:
            if key[0] in self.key_pressed:
                self.robot_x += key[1]
                self.robot_y += key[2]
     
        self.game_instance.screen.blit(self.robot, (self.robot_x, self.robot_y))

        self.robot_x = min(self.robot_x, self.game_instance.width - self.robot.get_width())
        self.robot_x = max(self.robot_x, 0)

    def get_coordinates(self):
        return (self.robot_x, self.robot_y)
    
    def get_width(self):
        return self.robot.get_width()

class RainingItem:
    def __init__(self, game_instance: RainingCoins, image: pg.image):
        self.game_instance = game_instance
        self._image = image
        self._count = 0
        self._frequency = 20
        self._speed = 2
        self._positions = self.start_positions()

    def start_positions(self):
        return [[-9001, self.game_instance.height] for i in range(self._frequency)]

    def draw(self):
        for i in range(self._frequency):
            current_item = self._positions[i]
            if self.detect_collision(self.game_instance.robot, i):
                self.collide_condition(i)
            self.monster_count(i)
            if current_item[1] < self.floor():
                current_item[1] += self._speed
            else:
                self.floor_boundary(current_item, i)

        for i in range(self._frequency):
            self.game_instance.screen.blit(self._image, (self._positions[i][0], self._positions[i][1]))

    def randomize_pos(self):
        return [randint(0, self.game_instance.width - self.image_width()), -randint(100, 1000)]

    # Hook Method
    def floor(self):
        pass

    # Hook Method
    def collide_condition(self):
        pass

    # Hook Method
    def monster_count(self, i: int):
        pass

    # Hook Method
    # Monsters disappear
    # Coins stay on the floor
    def floor_boundary(self, current_item: list[int], index: int):
        pass

    def detect_collision(self, robot: Robot, item_index: int):
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

    def start_positions(self):
        return [self.randomize_pos() for i in range(self._frequency)]

    def floor(self):
        return 430 - self.image_height()

    def collide_condition(self, i: int):
        pass

class Monster(RainingItem):
    def __init__(self, game_instance: RainingCoins, monster: pg.image):
        super().__init__(game_instance, monster)
        self.visited = [False] * self._frequency

    def floor(self):
        return self.game_instance.height

    def collide_condition(self, i: int):
        sys.exit()

    def monster_count(self, i: int):
        if (not self.visited[i] and self._positions[i][1] >= 0 and \
        self._positions[i][1] + self._image.get_height() <= self.game_instance.height):
            self._count += 1
            self.visited[i] = True

    def floor_boundary(self, current_monster: list[int], i: int):
        current_monster[0], current_monster[1] = self.randomize_pos()
        self.visited[i] = False

###########################################################################################################################

if __name__ == "__main__":
    rc = RainingCoins()
    rc.monster.set_frequency(8)
    rc.play_game()
