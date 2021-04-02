import pygame

from gamedata import GameData
from gamestate import GameState, GameStateID


class GameWon(GameState):

    def __init__(self, data: GameData) -> None:
        super().__init__(data)
        self.id = GameStateID.WINNER_WINNER
        self.user_clicked = False
        self.win_message = "Congratulations, you won!"
        self.back_to_menu = "Click to return to the main menu"

    def input(self, event: pygame.event) -> None:
        """ Checks to see if user clicks button and set user_clicked """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.user_clicked = True

    def update(self, dt: float) -> GameStateID:
        """ If user_clicked go to game menu else return WINNER_WINNER """
        if self.user_clicked:
            self.user_clicked = False
            return GameStateID.START_MENU
        else:
            return GameStateID.WINNER_WINNER

    def render(self, screen: pygame.Surface) -> None:
        """ Renders the game won message / assets """
        win_msg = self.gamedata.fonts["menu"].render(f'{self.win_message}', True, (0, 0, 0))
        return_msg = self.gamedata.fonts["debug"].render(f'{self.back_to_menu}', True, (0, 0, 0))

        screen.blit(win_msg, (100, 325))
        screen.blit(return_msg, (500, 470))
