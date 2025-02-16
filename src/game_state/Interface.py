from typing import TYPE_CHECKING
import pygame as pg

if TYPE_CHECKING:
    from main import RainingCoins

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

class UI:
    def __init__(self, game_instance: "RainingCoins"):
        self.__game_instance = game_instance
        self.__game_font = pg.font.SysFont("Arial", 24)

    def draw_ui(self):
        self.__game_instance.time.draw_time()

        if self.__game_instance.state.is_game_clear():
            self.__game_instance.ui.draw_game_state("You win!")
        elif self.__game_instance.state.is_game_over():
            self.__game_instance.ui.draw_game_state("GAME OVER")

        self.draw_text("Esc = exit game", 20, 440)
        pg.draw.line(self.__game_instance.screen.screen, (255, 0, 0), (0, 430), (self.__game_instance.screen.width, 430), 3)

        self.draw_text(f"x{self.__game_instance.coin.count}", 520, 440)
        self.__game_instance.screen.render_screen(self.draw_icon(self.__game_instance.coin.image), 490, 445)

        self.draw_text(f"x{self.__game_instance.monster.count}", 430, 440)
        self.__game_instance.screen.render_screen(self.draw_icon(self.__game_instance.monster.image), 400, 435)
        
    def draw_game_state(self, state: str):
        state_font = pg.font.SysFont("Arial", 69)
        text = self.__game_text(f"{state}", state_font)

        center_x = self.__game_instance.screen.width / 2 - text.get_size()[0] / 2
        center_y = self.__game_instance.screen.height / 2 - text.get_size()[1] / 2

        self.__game_instance.screen.render_screen(text, center_x, center_y)

    def draw_text(self, hud: str, x: int, y: int):
        self.__game_instance.screen.render_screen(self.__game_text(hud, self.__game_font), x, y)

    def draw_icon(self, image: pg.image):
        return pg.transform.scale(image, (image.get_size()[0] // 2, image.get_size()[1] // 2))

    def __game_text(self, hud: str, font: pg.font):
        return font.render(hud, True, (255, 0, 0))