from __future__ import annotations

__all__ = ["StartMenuView"]

import arcade
import arcade.gui


class StartMenuView(arcade.View):
    """ `banjo.views.StartMenuView` is the starting screen menu view for the game.
    This provides a simple menu interface for the player to start the game, set
    options, view credits, or exit the game.

    Attributes
    ----------
    `manager` : arcade.gui.UIManager
        The UI manager that handles the GUI elements in the menu view.
    `layout` : arcade.gui.UILayout
        The layout that contains the buttons and other UI elements in the menu view.
    `game_view` : banjo.views.GameView
        The game view that is displayed when the player starts the game.
    `ost_player` : pyglet.media.Player
        The original soundtrack player in the menu view.
    """
    def __init__(self) -> None:
        """ Initialize the menu view.
        """
        from banjo.views import GameView

        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.layout = self.setup_layout()
        self.game_view = GameView()
        self.ost_player = arcade.play_sound(
            arcade.sound.load_sound("sounds/Downstream Rampage.mp3", streaming=True)
        )

    def setup_buttons(self) -> list[arcade.gui.UIFlatButton]:
        """ Setup the buttons for the menu view.

        Returns
        -------
        list[arcade.gui.UIFlatButton]
            A list of buttons for the menu.
        """
        start_button = arcade.gui.UIFlatButton(
            text="Start Game", width=200, height=50
        )
        credits_button = arcade.gui.UIFlatButton(
            text="Credits", width=200, height=50
        )
        quit_button = arcade.gui.UIFlatButton(
            text="Quit", width=200, height=50
        )

        @start_button.event("on_click")
        def on_click_start_button(event):
            self.game_view.setup()
            self.window.show_view(self.game_view)
            arcade.stop_sound(self.ost_player) # type: ignore

        @credits_button.event("on_click")
        def on_click_credits_button(event):
            from banjo.views import CreditsView

            self.window.show_view(CreditsView())
            arcade.stop_sound(self.ost_player) # type: ignore

        @quit_button.event("on_click")
        def on_click_quit_button(event):
            arcade.exit()

        return [start_button, credits_button, quit_button]

    def setup_layout(self) -> arcade.gui.UILayout:
        """ Setup the layout for the menu view.

        Returns
        -------
        arcade.gui.UILayout
            The layout for the menu view.
        """
        buttons = self.setup_buttons()
        layout = arcade.gui.UIBoxLayout(
            vertical=True, space_between=10, align="center"
        )

        for button in buttons:
            layout.add(button)

        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())

        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=layout,
        )

        return layout

    def on_show_view(self) -> None:
        self.manager.enable()

    def on_draw(self) -> None:
        self.clear()
        self.manager.draw()