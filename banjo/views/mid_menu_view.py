from __future__ import annotations

__all__ = ["MidMenuView"]

import arcade
import arcade.gui


class MidMenuView(arcade.View):
    """ `banjo.views.MidMenuView` is the mid-game menu view for the game.
    This provides a simple menu interface for the player to resume the game,
    quit to the main menu, or quit the game entirely.

    Parameters
    ----------
    `game_view` : arcade.View
        An instance of `GameView` that will be displayed when the player starts the game.

    Attributes
    ----------
    `manager` : arcade.gui.UIManager
        The UI manager that handles the GUI elements in the menu view.
    `layout` : arcade.gui.UILayout
        The layout that contains the buttons and other UI elements in the menu view.
    `game_view` : GameView
        The game view that is displayed when the player starts the game.

    Raises
    ------
    TypeError
        - If `game_view` is not an instance of `GameView`.
    """
    def __init__(
            self,
            game_view: arcade.View
        ) -> None:
        """ Initialize the menu view.
        """
        from banjo.views import GameView

        super().__init__()

        if not isinstance(game_view, GameView):
            raise TypeError(
                "game_view must be an instance of GameView"
            )

        self.manager = arcade.gui.UIManager()
        self.layout = self.setup_layout()
        self.game_view = game_view

    def setup_buttons(self) -> list[arcade.gui.UIFlatButton]:
        """ Setup the buttons for the menu view.

        Returns
        -------
        list[arcade.gui.UIFlatButton]
            A list of buttons for the menu.
        """
        start_button = arcade.gui.UIFlatButton(
            text="Resume", width=200, height=50
        )
        quit_to_menu_button = arcade.gui.UIFlatButton(
            text="Quit to Menu", width=200, height=50
        )

        @start_button.event("on_click")
        def on_click_resume_button(event):
            self.window.show_view(self.game_view)

        @quit_to_menu_button.event("on_click")
        def on_click_quit_to_menu_button(event):
            from banjo.views import StartMenuView

            self.window.show_view(StartMenuView())

        return [start_button, quit_to_menu_button]

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

    def on_key_press(
            self,
            symbol: int,
            modifiers: int
        ) -> bool | None:

        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)