import pygame

from gamestate import GameState
from gamestate import GameStateID
from gamedata import GameData
from enum import Enum


class MenuID(Enum):

    START_GAME = 1
    QUIT = 2
    START_MENU = 3


class GameMenu(GameState):

    def __init__(self, gamedata: GameData) -> None:
        super().__init__(gamedata)
        self.id = GameStateID.START_MENU
        self.menu_id = MenuID.START_MENU
        self.new_game_selected = True
        self.new_game_option = "Start new game"
        self.quit_game_option = "Quit game"

    def input(self, event: pygame.event) -> None:
        """ Handles the user input to select menu items """
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_UP or event.key == pygame.K_DOWN):
            self.new_game_selected = not self.new_game_selected

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if self.new_game_selected:
                self.menu_id = self.menu_id.START_GAME
            else:
                self.menu_id = self.menu_id.QUIT

    def update(self, dt: float) -> GameStateID:
        """ If menu item is selected transition to appropriate state else return START_MENU """
        if self.menu_id is MenuID.START_MENU:
            return GameStateID.START_MENU
        elif self.menu_id is MenuID.START_GAME:
            self.menu_id = MenuID.START_MENU
            return GameStateID.GAMEPLAY
        elif self.menu_id is MenuID.QUIT:
            self.menu_id = MenuID.START_MENU
            return GameStateID.EXIT

    def render(self, screen: pygame.Surface) -> None:
        """ Use pygame to draw the menu """
        screen.fill((0, 0, 0))

        if self.new_game_selected:
            new_game = self.gamedata.fonts["menu"].render(f'> {self.new_game_option}', True, (200, 200, 200))
            quit_game = self.gamedata.fonts["menu"].render(f'   {self.quit_game_option}', True, (200, 200, 200))
        else:
            new_game = self.gamedata.fonts["menu"].render(f'   {self.new_game_option}', True, (200, 200, 200))
            quit_game = self.gamedata.fonts["menu"].render(f'> {self.quit_game_option}', True, (200, 200, 200))

        screen.blit(new_game, (300, 325))
        screen.blit(quit_game, (300, 475))

