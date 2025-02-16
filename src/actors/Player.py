from typing import TYPE_CHECKING
from actors.DrawObject import DrawObject
import pygame as pg

if TYPE_CHECKING:
    from main import RainingCoins

class Robot(DrawObject):
    def __init__(self, game_instance: "RainingCoins", robot: pg.image):
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