from __future__ import annotations

__all__ = ["WinView"]

import arcade


class WinView(arcade.View):
    """ `banjo.views.WinView` is the class that represents the win view
    where the game is displayed after the player wins. It is a subclass of
    `arcade.View` and has additional functionality to handle player input
    and display the win message.

    Attributes
    ----------
    `text_win` : arcade.Text
        The text displayed when the player wins.
    `text_instruction` : arcade.Text
        The text displayed to instruct the player to try again.
    """
    def __init__(self) -> None:
        """ Initialize the game over view.
        """
        super().__init__()

        self.text_game_over = arcade.Text(
            "Banjo made it downstream", 100, 200, arcade.color.GREEN, 24
        )
        self.text_instruction = arcade.Text(
            "Press any key for main menu", 100, 150, arcade.color.WHITE, 18
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

        from banjo.views import StartMenuView

        self.window.show_view(StartMenuView())