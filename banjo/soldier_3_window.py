from __future__ import annotations

__all__ = ["GameWindow"]

import arcade
from banjo.characters.soldier_3 import WALKING_VELOCITY, RUNNING_VELOCITY
from banjo import Soldier3

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Soldier3"


class GameWindow(arcade.Window):
    """ `banjo.GameWindow` is the class that represents the game window
    where the game is displayed. It is a subclass of `arcade.Window` and
    has additional functionality to handle player input and game logic.

    Attributes
    ----------
    `left_pressed` : bool
        A boolean representing whether the left arrow key is pressed.
    `right_pressed` : bool
        A boolean representing whether the right arrow key is pressed.
    `shift_pressed` : bool
        A boolean representing whether the shift key is pressed.
    `m_pressed` : bool
        A boolean representing whether the 'M' key is pressed.
    `space_pressed` : bool
        A boolean representing whether the space key is pressed.
    `d_pressed` : bool
        A boolean representing whether the 'D' key is pressed.

    `player_list` : arcade.SpriteList
        A list of all the sprites in the game.
    `player` : Soldier3
        The player character in the game.
    `physics_engine` : arcade.PymunkPhysicsEngine
        The physics engine used to handle player movement.

    Usage
    -----
    >>> window = GameWindow()
    >>> window.setup()
    >>> window.run()
    """
    def __init__(self) -> None:
        """ Initialize the game window.
        """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.set_location(400, 200)

        arcade.set_background_color(arcade.color.BLACK)

        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.k_pressed: bool = False
        self.r_pressed: bool = False
        self.shift_pressed: bool = False
        self.ctrl_pressed: bool = False
        self.m_pressed: bool = False
        self.d_pressed: bool = False
        self.h_pressed: bool = False

        self.physics_engine = arcade.PymunkPhysicsEngine()

    def setup(self) -> None:
        """ Set up the game window.
        """
        self.player_list: arcade.SpriteList = arcade.SpriteList()
        self.player = Soldier3()

        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2

        self.player_list.append(self.player)

        self.physics_engine.add_sprite(self.player)

    def on_draw(self) -> None:
        self.clear()
        self.player_list.draw()

    def on_update(
            self,
            delta_time: float
        ) -> None:

        self.player_list.update_animation(delta_time)

        if self.d_pressed:
            self.player.current_animation = "death"
            return

        if self.m_pressed:
            self.player.current_animation = "melee"
            return

        if self.k_pressed:
            if self.shift_pressed:
                self.player.current_animation = "aim_fire"
            else:
                self.player.current_animation = "crouch_fire"
            return

        if self.r_pressed:
            self.player.current_animation = "reload"
            return

        if self.h_pressed:
            self.player.current_animation = "hurt"
            return

        if self.left_pressed and not self.right_pressed:
            if self.player.character_face_direction == 0:
                self.player.turn()

            if self.shift_pressed:
                self.player.current_animation = "run"
                self.physics_engine.set_velocity(self.player, (-RUNNING_VELOCITY, 0))
            else:
                self.player.current_animation = "walk"
                self.physics_engine.set_velocity(self.player, (-WALKING_VELOCITY, 0))

        elif self.right_pressed and not self.left_pressed:
            if self.player.character_face_direction == 1:
                self.player.turn()

            if self.shift_pressed:
                self.player.current_animation = "run"
                self.physics_engine.set_velocity(self.player, (RUNNING_VELOCITY, 0))
            else:
                self.player.current_animation = "walk"
                self.physics_engine.set_velocity(self.player, (WALKING_VELOCITY, 0))

        # Stop the player if no movement keys are pressed
        else:
            self.physics_engine.set_velocity(self.player, (0, 0))
            self.player.current_animation = "idle"

        self.physics_engine.step()

    def on_key_press(
            self,
            symbol,
            modifiers
        ) -> None:

        if symbol == arcade.key.LEFT:
            self.left_pressed = True
        elif symbol == arcade.key.RIGHT:
            self.right_pressed = True
        elif symbol == arcade.key.M:
            self.m_pressed = True
        elif symbol == arcade.key.K:
            self.k_pressed = True
        elif symbol == arcade.key.R:
            self.r_pressed = True
        elif symbol == arcade.key.LSHIFT:
            self.shift_pressed = True
        elif symbol == arcade.key.D:
            self.d_pressed = True
        elif symbol == arcade.key.H:
            self.h_pressed = True

    def on_key_release(
            self,
            symbol,
            modifiers
        ) -> None:

        if symbol == arcade.key.LEFT:
            self.left_pressed = False
        elif symbol == arcade.key.RIGHT:
            self.right_pressed = False
        elif symbol == arcade.key.M:
            self.m_pressed = False
        elif symbol == arcade.key.K:
            self.k_pressed = False
        elif symbol == arcade.key.R:
            self.r_pressed = False
        elif symbol == arcade.key.LSHIFT:
            self.shift_pressed = False
        elif symbol == arcade.key.H:
            self.h_pressed = False