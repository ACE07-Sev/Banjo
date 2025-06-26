from __future__ import annotations

__all__ = ["CreditsView"]

import arcade


class CreditsView(arcade.View):
    """ `banjo.views.CreditsView` is the class that represents the credits view
    where the credits of the game are displayed. It is a subclass of `arcade.View
    and has additional functionality to handle scrolling credits and returning
    to the main menu.

    Attributes
    ----------
    `credits_lines` : list[str]
        A list of strings representing the lines of credits to be displayed.
    `num_lines` : int
        The number of lines in the credits.
    `text_y` : float
        The vertical position of the text in the credits view.
    `scroll_speed` : float
        The speed at which the credits scroll vertically.
    """
    def __init__(self) -> None:
        """ Initialize the credits view.
        """
        super().__init__()

        credit_lines = [
            "Banjo",
            "",
            "Developed by:\n Amir Ali Malekani Nezhad \n",
            "Special Thanks:\n Gökçe Çimen \n",
            "",
            "Thank you for playing!",
        ]
        credit_lines.reverse()
        self.credits_lines = credit_lines
        self.num_lines = len(credit_lines)

        self.text_y = -self.num_lines * 30
        self.scroll_speed = 50

    def on_draw(self) -> None:
        self.clear()
        y = self.text_y
        center_x = self.window.width // 2

        for line in self.credits_lines:
            arcade.draw_text(
                line,
                center_x,
                y,
                font_size=20,
                anchor_x="center"
            )
            y += 30

        arcade.draw_text(
            "Press ESC to return to Main Menu",
            self.window.width // 2,
            20,
            font_size=14,
            anchor_x="center"
        )

    def on_update(
            self,
            delta_time: float
        ) -> None:

        self.text_y += self.scroll_speed * delta_time

        # Restart credits after they scroll off screen
        if self.text_y > self.window.height + self.num_lines * 30:
            self.text_y = -self.num_lines * 30

    def on_key_press(
            self,
            symbol: int,
            modifiers: int
        ) -> None:

        from banjo.views import StartMenuView

        if symbol == arcade.key.ESCAPE:
            self.window.show_view(StartMenuView())