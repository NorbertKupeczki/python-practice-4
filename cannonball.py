import pygame
CANNONBALL_SPEED = 8


class CannonBall(pygame.sprite.Sprite):
    """ A cannonball represents the projectiles used in the game.
    """

    def __init__(self, spawn: pygame.Vector2, dest: pygame.Vector2) -> None:
        """ Initialises the cannonball instance

        Args:
            spawn (pygame.Vector2): Where the cannonball originates from.
            dest (pygame.Vector2): It's intended destination.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("data/sprites/ship parts/cannonBall.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (spawn[0], spawn[1])
        self.destination = dest
        self.position = pygame.Vector2(spawn)

    def update(self, dt: float) -> None:
        """ Updates the cannonball instance using lerp. It will continue
        to lerp until it reaches it's destination. It would make sense to
        check if the vectors are equal before calculating the lerped vector.
        The sprite rectangles are drawn from the topleft, hence we update
        it's new position with the resultant lerp'd location

        Args:
            dt (float): The time between ticks.
        """
        lerped = self.position.lerp(self.destination, min(CANNONBALL_SPEED * dt, 1))
        self.position = lerped
        self.rect.topleft = self.position
