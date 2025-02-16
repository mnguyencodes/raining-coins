from typing import TYPE_CHECKING
from random import randint

if TYPE_CHECKING:
    from game_state.GameController import RainingCoins, Robot, pg

class DrawObject:
    def __init__(self, game_instance: "RainingCoins"):
        self._game_instance = game_instance

    def draw(self):
        self._render_object()
        if self._game_instance.time.is_time_up() or self._game_instance.state.is_game_over():
            return
        self._update_object_xy()

    def _render_object(self):
        pass

    def _update_object_xy(self):
        pass

class RainingItem(DrawObject):
    def __init__(self, game_instance: "RainingCoins", image: "pg.image"):
        super().__init__(game_instance)
        self._image = image
        self._count = 0
        self._frequency = 20
        self._speed = 2
        self._positions = self._start_positions()

    @property
    def count(self):
        return self._count
    
    @property
    def image(self):
        return self._image

    def set_frequency(self, frequency: int):
        self._frequency = frequency
    
    def set_speed(self, speed: int):
        self._speed = speed

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

    def __detect_collision(self, robot: "Robot", item_index: int):
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