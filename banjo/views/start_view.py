from __future__ import annotations

__all__ = ["StartView"]

import arcade


class StartView(arcade.View):
    """ The start view of the game.
    """
    def __init__(self):
        super().__init__()

    def on_show(self) -> None:
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self) -> None:
        self.texts = [
            arcade.Text("CODENAME: Banjo", 100, 200, arcade.color.WHITE, 24),
            arcade.Text("Press any key to start", 100, 150, arcade.color.WHITE, 18)
        ]

    def on_draw(self) -> None:
        self.clear()
        for text in self.texts:
            text.draw()

    def on_key_press(
            self,
            symbol: int,
            modifiers: int
        ) -> None:

        if symbol == arcade.key.ENTER or symbol == arcade.key.SPACE:
            from banjo.views.game_view import GameView

            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)