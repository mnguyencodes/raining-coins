import pygame as pg
import sys
import path_utils as pu
from datetime import timedelta
from game_state.Interface import UI, Screen
from actors.Entities import Coin, Monster
from actors.Player import Robot

class RainingCoins:
    def __init__(self):
        self.__initialize_game()
        self.__initialize_assets()

    def __initialize_game(self):
        pg.init()
        pg.display.set_caption("RainingCoins")
        self.__ui = UI(self)
        self.__state = GameState(self)
        self.__screen = Screen()
        self.__time = Time(self)
        self.__clock = pg.time.Clock()

    @property
    def ui(self):
        return self.__ui

    @property
    def state(self):
        return self.__state

    @property
    def screen(self):
        return self.__screen

    @property
    def time(self):
        return self.__time

    def __initialize_assets(self):
        ASSETS_DIR = pu.os.path.join(pu.get_parent_dir(pu.root_dir()), "assets")        
        robot = pg.image.load(f"{ASSETS_DIR}\\robot.png")
        self.__robot = Robot(self, robot)

        coin = pg.image.load(f"{ASSETS_DIR}\\coin.png")
        self.__coin = Coin(self, coin)

        monster = pg.image.load(f"{ASSETS_DIR}\\monster.png")
        self.__monster = Monster(self, monster)

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

    def exit_game(self):
        sys.exit()

    def __check_events(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.exit_game()
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
        self.__ui.draw_ui()

        self.__clock.tick(60)
        pg.display.flip()   

    def __draw_screen_test(self):
        self.__screen.clear_screen()
        self.__ui.draw_ui()
        self.__screen.render_screen()
        pg.display.flip()

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
        self.__game_instance.ui.draw_text(f"{minutes}:{seconds:02}", 580, 440)

    def get_time_ticks(self):
        return pg.time.get_ticks()

    def __calculate_time_remaining(self):
        current_ticks = (pg.time.get_ticks()
            if not self.__game_instance.state.is_game_over() 
            else self.__game_instance.state.get_end_time())
        
        elapsed_seconds = (current_ticks - self.__start_ticks) // 1000
        time_remaining = self.__timer - timedelta(seconds = elapsed_seconds)
        total_seconds = int(time_remaining.total_seconds())
        minutes, seconds = divmod(total_seconds, 60)

        if total_seconds <= 0:
            self.__time_up = True
            self.__game_instance.state.game_clear()
            return (0, 0)

        return (minutes, seconds)

class GameState:
    def __init__(self, game_instance: RainingCoins):
        self.__game_instance = game_instance
        self.__game_clear = False
        self.__game_over = False

    def game_clear(self):
        self.__game_clear = True

    def game_over(self):
        self.__game_over = True
        self.__end_time = self.__game_instance.time.get_time_ticks()        

    def get_end_time(self):
        return self.__end_time

    def is_game_clear(self):
        return self.__game_clear
    
    def is_game_over(self):
        return self.__game_over