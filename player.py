from enum import IntEnum

import pygame
from typing import List
from fsm import FSM
from shipcondition import ShipCondition
from math import atan2, degrees

PLAYER_SPEED = 0.5


class Player(pygame.sprite.Sprite):
    """Our Player's Pirate Ship!
    """

    def __init__(self) -> None:
        super().__init__()

        # we have to store base surfaces for each kind of ship condition
        filenames = ["data/sprites/ships/ship (2).png",
                     "data/sprites/ships/ship (8).png",
                     "data/sprites/ships/ship (14).png",
                     "data/sprites/ships/ship (20).png"]

        self.base_list = [pygame.image.load(filename).convert_alpha() for filename in filenames]
        self.base = self.base_list[0]
        self.image = self.base.copy()
        self.rect = self.image.get_rect()

        # current position and previous
        self._position = [0.0, 0.0]
        self._old_position = self.position
        self.destination = self.position

        # player game data/state
        self.mouse_down = False
        self.score = 0
        self.path = []
        self.move_vector = [0, 0]

        self.fsm = FSM()
        self.fsm.setstate(self.update_healthy)
        self.prev_ship_condition = ShipCondition.HEALTHY
        self.ship_condition = ShipCondition.HEALTHY
        self.hp = 10

        # set the initial state
        self.prev_ship_condition = ShipCondition.HEALTHY
        self.ship_condition = ShipCondition.HEALTHY

    @property
    def position(self) -> List[float]:
        return list(self._position)

    @position.setter
    def position(self, value: List[float]) -> None:
        self._position = list(value)

    def update(self, dt: float) -> None:
        """ Updates the player's ship

        This function will attempt to lerp the player to their new
        destination. It will control the speed at which that happens
        using PLAYER_SPEED. Lerping has its issues but is a good start
        to make the game playable. The update function will also redraw
        the ship if it's condition changes.

        Args:
            dt (float): The time elapsed since last tick
        """
        # self._old_position = self._position[:]

        self.move_ship()

        self.rect.topleft = self._position

        self.fsm.update()

        if self.ship_condition != self.prev_ship_condition:
            self.prev_ship_condition = self.ship_condition
            self.redraw()

    def move_back(self, dt: float) -> None:
        """If called after an update, the sprite will move back"""
        self._position = self._old_position
        self.destination = self._old_position
        self.rect.topleft = self._position

    def rotate(self, angle: float) -> None:
        """rotates the image so that it always points to direction of travel"""
        self.image = pygame.transform.rotozoom(self.base, 90 - angle, 1)
        x, y = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def redraw(self) -> None:
        """redraws the ship based on its current condition

        There's a bug inside this function, see if you can locate it
        and resolve it. It's easy to replicate by altering your ship's
        condition whilst pointing at a new destination.
        """
        if self.ship_condition <= ShipCondition.SUNK:
            self.base = self.base_list[self.ship_condition]
            self.image = self.base.copy()
            self.rect = self.image.get_rect()

    def update_healthy(self):
        """ The first of your FSM functions, this one is complete """
        self.ship_condition = ShipCondition.HEALTHY
        if self.hp <= 6:
            self.fsm.setstate(self.update_damaged)

    def update_damaged(self):
        """ Create the logic here for the ship when it's damaged """
        self.ship_condition = ShipCondition.DAMAGED
        if self.hp <= 3:
            self.fsm.setstate(self.update_very_damaged)

    def update_very_damaged(self):
        """ Create the logic here for the ship when it's very damaged """
        self.ship_condition = ShipCondition.VERY_DAMAGED
        if self.hp <= 0:
            self.fsm.setstate(self.dead)

    def dead(self):
        """ Create the logic here for the ship is sunk """
        self.ship_condition = ShipCondition.SUNK

    def move_ship(self):
        if self.position == self.destination and len(self.path) > 0:
            next_destination = self.path.pop(0)
            self.destination[0] = int(next_destination[0])
            self.destination[1] = int(next_destination[1])

            self.move_vector[0] = (int(self._position[0]) - self.destination[0]) / 128
            self.move_vector[1] = (int(self._position[1]) - self.destination[1]) / 128

            dx = self.destination[0] - self.position[0]
            dy = self.destination[1] - self.position[1]
            rad = atan2(dy, dx)
            self.rotate(degrees(rad))
        elif self.position == self.destination:
            self.move_vector = [0, 0]
        else:
            self._position[0] = self.position[0] - self.move_vector[0] * PLAYER_SPEED
            self._position[1] = self.position[1] - self.move_vector[1] * PLAYER_SPEED
