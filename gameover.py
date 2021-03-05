import pygame

from gamestate import GameState
from gamestate import GameStateID
from gamedata import GameData


class GameOver(GameState):

    def __init__(self, data: GameData) -> None:
        super().__init__(data)
        self.id = GameStateID.GAME_OVER
        self.user_clicked = False

    def update(self, dt: float) -> GameStateID:
        """ If user_clicked go to game menu else return GAME_OVER"""
        print("updating")
        return GameStateID.GAME_OVER

    def render(self, screen: pygame.Surface) -> None:
        """ Renders the game lost message / assets """
        print("rendering")

    def input(self, event: pygame.event) -> None:
        """ Checks to see if user clicks button and set user_clicked """
        print("processing input")
