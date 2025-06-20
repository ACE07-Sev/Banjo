from __future__ import annotations

__all__ = ["GameOverView"]

import arcade


class GameOverView(arcade.View):
    """ The game over view.
    """
    def __init__(self):
        super().__init__()

    def on_show(self) -> None:
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self) -> None:
        self.clear()
        GAME_OVER = arcade.Text("'Target is eliminated. RTB...'", 100, 200, arcade.color.RED, 24)
        INSTRUCTION = arcade.Text("Press any key to try again", 100, 150, arcade.color.WHITE, 18)
        GAME_OVER.draw()
        INSTRUCTION.draw()

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