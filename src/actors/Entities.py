from typing import TYPE_CHECKING
from actors.DrawObject import RainingItem

if TYPE_CHECKING:
    from game_state.GameController import RainingCoins, pg

class Coin(RainingItem):
    def __init__(self, game_instance: "RainingCoins", coin: "pg.image"):
        super().__init__(game_instance, coin)

    def _start_positions(self):
        return [self._randomize_pos() for i in range(self._frequency)]

    def _collide_condition(self, i: int):
        self._positions[i][0], self._positions[i][1] = self._randomize_pos()
        self._count += 1

class Monster(RainingItem):
    def __init__(self, game_instance: "RainingCoins", monster: "pg.image"):
        super().__init__(game_instance, monster)
        self.__visited = [False] * self._frequency

    def _collide_condition(self, i: int):
        self._game_instance.state.game_over()

    def _monster_count(self, i: int):
        if (not self.__visited[i] and self._positions[i][1] >= 0 and \
        self._positions[i][1] + self._image.get_height() <= self._game_instance.screen.height):
            self._count += 1
            self.__visited[i] = True

    def _floor_boundary(self, current_monster: list[int], i: int):
        current_monster[0], current_monster[1] = self._randomize_pos()
        self.__visited[i] = False