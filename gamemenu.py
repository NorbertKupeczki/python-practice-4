import pygame

from gamestate import GameState
from gamestate import GameStateID
from gamedata import GameData


class GameMenu(GameState):

    def __init__(self, gamedata: GameData) -> None:
        super().__init__(gamedata)
        self.id = GameStateID.START_MENU

    def input(self, event: pygame.event) -> None:
        """ Handles the user input to select menu items """
        print("processing input")

    def update(self, dt: float) -> GameStateID:
        """ If menu item is selected transition to appropriate state else return START_MENU """
        print("updating")
        return GameStateID.START_MENU

    def render(self, screen: pygame.Surface) -> None:
        """ Use pygame to draw the menu """
        print("rendering")
