from __future__ import annotations

__all__ = ["GameOverView"]

import arcade


class GameOverView(arcade.View):
    """ The game over view.
    """
    def __init__(self) -> None:
        """ Initialize the game over view.
        """
        super().__init__()

        self.text_game_over = arcade.Text(
            "'Target is eliminated. RTB...'", 100, 200, arcade.color.RED, 24
        )
        self.text_instruction = arcade.Text(
            "Press any key to try again", 100, 150, arcade.color.WHITE, 18
        )

    def on_draw(self) -> None:
        self.clear()
        self.text_game_over.draw()
        self.text_instruction.draw()

    def on_show_view(self) -> None:
        arcade.Camera2D().use()

    def on_key_press(
            self,
            symbol: int,
            modifiers: int
        ) -> None:

        from banjo.views import GameView

        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)