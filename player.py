from enum import IntEnum

import pygame
from typing import List
from shipcondition import ShipCondition

PLAYER_SPEED = 1


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
        self._old_position = self._position[:]

        dest_vector = pygame.Vector2(self.destination[0], self.destination[1])
        pos_vector = pygame.Vector2(self._position[0], self._position[1])

        lerped = pos_vector.lerp(dest_vector, min(PLAYER_SPEED * dt, 1))
        self._position[0] = lerped[0]
        self._position[1] = lerped[1]

        self.rect.topleft = self._position

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
        if self.ship_condition < 4:
            self.base = self.base_list[self.ship_condition]
            self.image = self.base.copy()
            self.rect = self.image.get_rect()
