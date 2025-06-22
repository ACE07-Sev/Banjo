from __future__ import annotations

__all__ = ["StartView"]

import arcade


class StartView(arcade.View):
    """ The start view of the game.
    """
    def __init__(self) -> None:
        """ Initialize the start view.
        """
        super().__init__()

        self.title = arcade.Text(
            "CODENAME: Banjo", 100, 200, arcade.color.WHITE, 24
        )
        self.instruction = arcade.Text(
            "Press any key to start", 100, 150, arcade.color.WHITE, 18
        )

    def on_draw(self) -> None:
        self.clear()
        self.title.draw()
        self.instruction.draw()

    def on_show_view(self) -> None:
        arcade.Camera2D().use()

    def on_key_press(
            self,
            symbol: int,
            modifiers: int
        ) -> None:

        if symbol == arcade.key.ENTER or symbol == arcade.key.SPACE:
            from banjo.views import GameView

            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)