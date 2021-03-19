# system libraries
import os
from collections import deque
from pathlib import Path

# pygame and tile map
import pygame
import pyscroll
import pyscroll.data
from pygame.locals import VIDEORESIZE

# https://github.com/bitcraft/pytmx
from pytmx import pytmx
from pytmx.util_pygame import load_pygame

# user defined ones
from gameplay import GamePlay
from gamestate import GameStateID
from gamemenu import GameMenu
from gamedata import GameData
from gamewon import GameWon
from gameover import GameOver

# define configuration variables here
CURRENT_DIR = Path(__file__).parent
RESOURCES_DIR = CURRENT_DIR / "data"


# simple wrapper to keep the screen resizeable
def initScreen(width: int, height: int) -> pygame.Surface:
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    return screen


def getPath(filename):
    return os.path.join(RESOURCES_DIR, filename)


class PirateGame:
    """ This class is your most excellent Pirate game.

    This class is responsible for loading data, sharing it,
    creating a scrollable map, initialising audio and creating
    the initial game state to use. For the map a pyscroll group
    will be used to render the sprites.. see GamePlay
    """

    def __init__(self) -> None:
        """ Initialise the game here

        Sets sane values for the game and creates the window size.
        I've gone for a typical 16:9 aspect ratio here. Remember
        to use functions when initialising more complex data structures
        i.e. audio or the map
        """
        self.width = 1920
        self.height = 1080
        self.costs = None
        self.gamedata = GameData()
        self.gamedata.fonts['scoreboard'] = pygame.font.Font('data/fonts/ErbosDraco1StNbpRegular-99V5.ttf', 72)
        self.gamedata.fonts['menu'] = pygame.font.Font(pygame.font.get_default_font(), 128)
        self.gamedata.fonts['debug'] = pygame.font.Font(pygame.font.get_default_font(), 18)
        self.screen = initScreen(self.width, self.height)
        self.background_colour = (100, 149, 237)
        self.screen.fill(self.background_colour)
        self.initAudio()
        self.loadMap()
        self.current_state = GameMenu(self.gamedata)
        self.running = False

    def initAudio(self) -> None:
        """ Initialises the audio

        At present only background audio has been provided,
        but you could choose to load additional sound effects
        and store them as part of the game data
        """
        print('init =', pygame.mixer.get_init())
        print('channels =', pygame.mixer.get_num_channels())
        self.gamedata.background_audio = pygame.mixer.Sound('data/audio/ambient.wav')
        self.gamedata.background_audio.play(-1)
        self.gamedata.background_audio.set_volume(self.gamedata.background_volume)
        print('length =', self.gamedata.background_audio.get_length())

    def loadMap(self) -> None:
        """ Loads the tiled map

        In order for your A* pathfinding to work you will need to
        store the weights associated with the tiles. You can do this
        programmatically or via properties using the editor. Load
        the weights here though.
        """
        # loads the map data
        tmx_data = load_pygame("./data/worldmap.tmx")
        map_data = pyscroll.TiledMapData(tmx_data)

        # the map stores collision rects with the islands
        for obj in tmx_data.objects:
            self.gamedata.gamemap.islands.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # generate the path finding map
        self.gamedata.gamemap.costs = [[0] * tmx_data.width for _ in range(tmx_data.height)]
        for layer in tmx_data.layers:
            if isinstance(layer, pytmx.TiledTileLayer):

                if "cost" in layer.properties:
                    cost = layer.properties["cost"]
                else:
                    continue

                for x, y, _ in layer.tiles():
                    self.gamedata.gamemap.costs[y][x] += cost

        # Make the scrolling layer
        self.gamedata.gamemap.map = pyscroll.BufferedRenderer(map_data, self.screen.get_size())

    def input_handler(self, event) -> None:
        """ Handles input events sent by pygame

        In a typical state system, we actually delegate these inputs
        to the active state. This allows the game to simply proxy
        on inputs to any active states.

        Args:
            event (pygame.Event): The input event
        """

        # mute background audio
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            print(self.gamedata.background_audio.get_volume())
            self.gamedata.background_audio.set_volume(self.gamedata.background_volume - self.gamedata.background_audio.get_volume())
            return

        # exit game
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.running = False
            return

        self.current_state.input(event)

    def update(self, dt: float) -> None:
        """ Updates the game

        The update function is the heart of the game. It processes
        the message pump and looks to forward game events on
        accordingly. Use delta time (dt) to maintain consistent
        animation speeds.

        Args:
            dt (float): The time elapsed since the previous tick
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif (
                event.type == pygame.MOUSEBUTTONDOWN or
                event.type == pygame.MOUSEBUTTONUP or
                event.type == pygame.MOUSEMOTION
            ):
                self.input_handler(event)

            elif event.type == pygame.KEYDOWN:
                self.input_handler(event)

            elif event.type == VIDEORESIZE:
                self.screen = initScreen(event.w, event.h)
                self.gamedata.gamemap.map.set_size((event.w, event.h))

        # delegate the update logic to the active state
        new_state = self.current_state.update(dt)
        if self.current_state.id != new_state:
            if new_state is GameStateID.START_MENU:
                self.current_state = GameMenu(self.gamedata)
            elif new_state is GameStateID.GAMEPLAY:
                self.current_state = GamePlay(self.gamedata)
            elif new_state is GameStateID.GAME_OVER:
                self.current_state = GameOver(self.gamedata)
            elif new_state is GameStateID.WINNER_WINNER:
                self.current_state = GameWon(self.gamedata)
            elif new_state is GameStateID.EXIT:
                self.running = False

    def render(self) -> None:
        """ Renders the active game state
        """
        self.current_state.render(self.screen)
        pygame.display.flip()

    def run(self) -> None:
        """Run the game loop"""
        clock = pygame.time.Clock()
        times = deque(maxlen=30)

        self.running = True
        while self.running:
            dt = clock.tick() / 1000.0
            times.append(clock.get_fps())

            self.update(dt)
            self.render()
        pygame.quit()


# initialises and starts the game running
def main() -> None:
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Arrrrr!!! Me Pirate Game!')

    try:
        game = PirateGame()
        game.run()
    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()

    exit(0)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(f"Launching PyGame")
    main()
