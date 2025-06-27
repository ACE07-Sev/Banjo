from __future__ import annotations

__all__ = ["GameWindow"]

import arcade
from banjo.views import StartMenuView

# Constants
# 720p is the resolution of the game
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Banjo"


class GameWindow(arcade.Window):
    """`banjo.GameWindow` is the class that represents the game window
    where the game is displayed. It is a subclass of `arcade.Window` and
    has additional functionality to handle player input and game logic.

    Usage
    -----
    >>> window = GameWindow()
    >>> window.setup()
    >>> window.run()
    """
    def __init__(self) -> None:
        """ Initialize the game window.
        """
        super().__init__(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            SCREEN_TITLE,
            antialiasing=False,
            vsync=True
        )
        self.show_view(StartMenuView())
        self.set_mouse_visible(True)

    def on_key_press(
            self,
            symbol: int,
            modifiers: int
        ) -> None:

        if symbol == arcade.key.F:
            self.set_fullscreen(fullscreen=not self.fullscreen)
            self.set_vsync(vsync=True)