from __future__ import annotations

__all__ = ["GameWindow"]

import arcade
from banjo.characters.banjo_player import WALKING_VELOCITY
from banjo import Banjo

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SCALE = 1.5
SCREEN_TITLE = "Banjo"


class GameWindow(arcade.Window):
    """`banjo.GameWindow` is the class that represents the game window
    where the game is displayed. It is a subclass of `arcade.Window` and
    has additional functionality to handle player input and game logic.

    Attributes
    ----------
    `left_pressed` : bool
        A boolean representing whether the left arrow key is pressed.
    `right_pressed` : bool
        A boolean representing whether the right arrow key is pressed.
    `m_pressed` : bool
        A boolean representing whether the 'M' key is pressed.
    `b_pressed` : bool
        A boolean representing whether the 'B' key is pressed.
    `d_pressed` : bool
        A boolean representing whether the 'D' key is pressed.
    `player` : Banjo
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
        """Initialize the game window."""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.set_location(400, 200)

        arcade.set_background_color(arcade.color.BLACK)

        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.m_pressed: bool = False
        self.b_pressed: bool = False
        self.d_pressed: bool = False

        self.physics_engine = arcade.PymunkPhysicsEngine()

    def setup(self) -> None:
        """Set up the game window."""
        self.player = Banjo()

        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2

        self.camera = arcade.Camera2D()

        tile_map = arcade.load_tilemap("./tiled/map.tmx", scaling=TILE_SCALE)
        self.scene = arcade.Scene.from_tilemap(tile_map)

        self.scene.add_sprite("Banjo", self.player)

        self.physics_engine.add_sprite(
            self.player,
            friction=self.player.friction,
            mass=self.player.mass,
            moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
            collision_type="player",
            gravity=(0, -1000),
            elasticity=0
        )

        self.physics_engine.add_sprite_list(
            self.scene["Concrete ground - Platform"],
            body_type=arcade.PymunkPhysicsEngine.STATIC,
            collision_type="ground",
        )
        self.physics_engine.add_sprite_list(
            self.scene["Sewer ground - Platform"],
            body_type=arcade.PymunkPhysicsEngine.STATIC,
            collision_type="ground",
        )

        self.physics_engine.add_sprite_list(
            self.scene["River ground - Platform"],
            body_type=arcade.PymunkPhysicsEngine.STATIC,
            collision_type="ground",
        )

    def on_draw(self) -> None:
        self.clear()

        self.camera.use()

        self.scene.draw()

    def on_update(self, delta_time: float) -> None:

        self.player.update_animation(delta_time)

        if self.d_pressed:
            self.player.current_animation = "death"
            return

        if self.m_pressed:
            self.player.current_animation = "melee"
            return

        if self.b_pressed:
            self.player.current_animation = "bark"
            return

        if self.left_pressed and not self.right_pressed:
            if self.player.character_face_direction == 0:
                self.player.turn()

            self.player.current_animation = "walk"
            self.physics_engine.set_horizontal_velocity(self.player, -WALKING_VELOCITY)

        elif self.right_pressed and not self.left_pressed:
            if self.player.character_face_direction == 1:
                self.player.turn()

            self.player.current_animation = "walk"
            self.physics_engine.set_horizontal_velocity(self.player, WALKING_VELOCITY)

        # Stop the player if no key is being pressed
        else:
            self.physics_engine.set_horizontal_velocity(self.player, 0)
            self.player.current_animation = "idle"

        self.camera.position = self.player.position

        self.physics_engine.step()

    def on_key_press(self, symbol, modifiers) -> None:

        if symbol == arcade.key.LEFT:
            self.left_pressed = True
        elif symbol == arcade.key.RIGHT:
            self.right_pressed = True
        elif symbol == arcade.key.M:
            self.m_pressed = True
        elif symbol == arcade.key.B:
            self.b_pressed = True
        elif symbol == arcade.key.D:
            self.d_pressed = True

    def on_key_release(self, symbol, modifiers) -> None:

        if symbol == arcade.key.LEFT:
            self.left_pressed = False
        elif symbol == arcade.key.RIGHT:
            self.right_pressed = False
        elif symbol == arcade.key.M:
            self.m_pressed = False
        elif symbol == arcade.key.B:
            self.b_pressed = False
