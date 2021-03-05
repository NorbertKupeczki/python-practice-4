import pygame
from gamedata import GameData
from gamestate import GameState, GameStateID


class GameWon(GameState):

    def __init__(self, data: GameData) -> None:
        super().__init__(data)
        self.id = GameStateID.WINNER_WINNER
        self.user_clicked = False

    def update(self, dt: float) -> GameStateID:
        """ If user_clicked go to game menu else return WINNER_WINNER """
        print("updating")
        return GameStateID.WINNER_WINNER

    def render(self, screen: pygame.Surface) -> None:
        """ Renders the game won message / assets """
        print("rendering")

    def input(self, event: pygame.event) -> None:
        """ Checks to see if user clicks button and set user_clicked """
        print("processing input")
