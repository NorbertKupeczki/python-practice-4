import pygame

from fsm import FSM
from shipcondition import ShipCondition


class Enemy(pygame.sprite.Sprite):
    """ An enemy ship

    This is a basic class to get you started. You will need to
    implement a number of improvements to it in order to complete
    the game. Provided within the class is an active FSM which
    needs to be updated when the enemy takes damage.
    """

    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        filenames = ["data/sprites/ships/ship (4).png",
                     "data/sprites/ships/ship (10).png",
                     "data/sprites/ships/ship (16).png",
                     "data/sprites/ships/ship (22).png"]

        self.base_list = [pygame.image.load(filename).convert_alpha() for filename in filenames]
        self.base = self.base_list[0]
        self.image = self.base.copy()
        self.rect = self.image.get_rect()

        self.rect.centerx = 0
        self.rect.centery = 0

        self.fsm = FSM()
        self.fsm.setstate(self.update_healthy)
        self.prev_ship_condition = ShipCondition.HEALTHY
        self.ship_condition = ShipCondition.HEALTHY
        self.hp = 10

    def update(self, dt: float) -> None:
        """ Updates the enemy and its FSM

        Calls the FSM for controlling the condition of the ship and will
        redraw the ship if it's current condition changes. This allows
        progressive damage to be shown using additional sprites.

        Args:
            dt (float): The amount of time elapsed between ticks
        """

        # update the fsm
        self.fsm.update()

        # if the ship's condition has changed we need to redraw it
        if self.ship_condition != self.prev_ship_condition:
            self.redraw()
            self.prev_ship_condition = self.ship_condition

    def redraw(self) -> None:
        """ Redraws the ship based on its condition """
        if self.ship_condition <= ShipCondition.SUNK:
            self.base = self.base_list[self.ship_condition]
            self.image = self.base.copy()

    def update_healthy(self):
        """ The first of your FSM functions, this one is complete """
        self.ship_condition = ShipCondition.HEALTHY
        if self.hp <= 6:
            self.fsm.setstate(self.update_damaged)

    def update_damaged(self):
        """ Create the logic here for the ship when it's damaged """
        self.ship_condition = ShipCondition.DAMAGED

    def update_very_damaged(self):
        """ Create the logic here for the ship when it's very damaged """
        self.ship_condition = ShipCondition.VERY_DAMAGED

    def deaded(self):
        """ Create the logic here for the ship is sunk """
        self.ship_condition = ShipCondition.SUNK
