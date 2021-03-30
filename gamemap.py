from typing import Tuple

import pygame


class GameMap:
    """ The view of the GameMap

    A useful class for storing all the tile information, collision
    rectangles and pathfinding weights. It also has a number of helper
    functions that can translate between world space and tile space.
    """

    def __init__(self):
        """ Initialises the game data class to sensible defaults"""
        self.islands = []   # collision rectangles
        self.map = None     # the tiled map
        self.costs = []     # pathfinding costs

    def inverse(self, mouse_pos: Tuple[int, int]) -> Tuple[int, int]:
        """ Translate screen co-ordinates need to world space

        The mouse's position is always reported in screen space. However,
        the world is larger than the screen, so we need to convert the
        screen position in to world-space to allow game logic to function
        correctly.

        Args:
            mouse_pos (pygame.event.pos): The mouse's position on screen
        """
        # currently doesn't support zoom
        return self.map.view_rect.x + mouse_pos[0], self.map.view_rect.y + mouse_pos[1]

    def tile(self, world_space: pygame.Vector2) -> Tuple[int, int]:
        """ Translate world space co-ordinates to tile location

        Given a position in the game world, this function will find the
        corresponding tile it resides in. This can be used to retrieve
        data from the cost map.

        Args:
            world_space (pygame.Vector2): The world-space position to convert
        """
        tile_size = self.map.data.tile_size
        return int(world_space[0] / tile_size[0]), int(world_space[1] / tile_size[1])

    def world(self, tile_xy: Tuple[int, int]) -> pygame.Vector2:
        """ Translate tile location to world space

        Given a tile location, this function will convert it to a
        position within the game world. It will always offset the
        position by the midpoint of the tile i.e. it's middle location

        Args:
            tile_xy (Tuple[int,int]):The tile location to convert
        """
        tile_size = self.map.data.tile_size

        return pygame.Vector2(
            ((tile_xy[0] + 1) * tile_size[0]) - (tile_size[0] * 0.5),
            ((tile_xy[1] + 1) * tile_size[1]) - (tile_size[1] * 0.5))

    def cost(self, world_space: pygame.Vector2):
        tilespace = self.tile(world_space)
        tile_cost = self.costs[tilespace[1]][tilespace[0]]
        return tile_cost
