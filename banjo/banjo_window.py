from __future__ import annotations

__all__ = ["GameWindow"]

import arcade
from banjo.characters import Banjo, Soldier1, Platoon
from banjo.resources.game_constants import LEFT_FACING, RIGHT_FACING
from banjo.resources.level_maps import SCENE, PLATFORMS
import random

# Constants
# 720p is the resolution of the game
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
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

    Usage
    -----
    >>> window = GameWindow()
    >>> window.setup()
    >>> window.run()
    """
    def __init__(self) -> None:
        """ Initialize the game window.
        """
        super().__init__(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            SCREEN_TITLE,
            antialiasing=False,
            vsync=True
        )
        self.set_location(400, 200)

        arcade.set_background_color(arcade.color.BLACK)

        # Player controller variables
        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.m_pressed: bool = False
        self.b_pressed: bool = False
        self.d_pressed: bool = False
        self.e_pressed: bool = False

        # Interactive map elements
        self.garage_broken: bool = False

    def setup(self) -> None:
        """Set up the game window.
        """
        for platform in PLATFORMS:
            platform.initialize()

        # Initialize the player and NPC
        self.player = Banjo()
        self.soldiers: arcade.SpriteList = Platoon([Soldier1() for _ in range(1)])

        # Set the initial position of the player and soldiers
        self.player.center_x = 2400
        self.player.center_y = SCREEN_HEIGHT // 2

        offset = 400
        for soldier in self.soldiers:
            soldier.center_x = SCREEN_WIDTH // 2 + offset
            soldier.center_y = SCREEN_HEIGHT // 2
            soldier.fsm.set_patrol_checkpoints([random.randint(500, 2000)])
            offset += 100

        # Set the initial position of the camera
        self.camera = arcade.Camera2D()

        # Load the map and set the scene
        self.scene = SCENE

        # Add Banjo to the scene and add his sprite
        # to the physics engine
        self.scene.add_sprite("Banjo", self.player)

        # Add Soldier NPCs to the scene and add their sprites
        # to the physics engine
        for i, soldier in enumerate(self.soldiers):
            self.scene.add_sprite(f"BRAVO-[1-{i}]", soldier)

    def on_draw(self) -> None:
        self.clear()
        self.camera.use()
        self.scene.draw()

    def handle_player_controls(self) -> None:
        """ Handle player controls.
        """
        # Cannot move the player if it is dead
        if self.player.is_dying:
            return

        # Maybe you want to die on command, I won't judge
        # It is not a bug, it is a feature >:)
        if self.d_pressed:
            self.player.current_animation = "dead"
            return

        if self.m_pressed:
            self.player.current_animation = "melee"

            if not self.garage_broken and arcade.check_for_collision_with_list(
                self.player, self.scene["Power Supply - Interactive"]
            ):
                self.scene.move_sprite_list_after(
                    "Power Supply - Broken", "Power Supply - Working"
                )
                self.scene.remove_sprite_list_by_name("Garage door - Animated")
                self.garage_broken = True
            return

        if self.b_pressed:
            self.player.current_animation = "bark"
            return

        if self.e_pressed:
            new_position = None

            if arcade.check_for_collision(
                self.player, self.scene["Sewer door left - Interactive"][0]
            ):
                new_position = self.scene["Sewer ground - Platform"][0].top
            for ladder in self.scene["Ladder left - Interactive"]:
                if arcade.check_for_collision(self.player, ladder):
                    new_position = self.scene["Concrete ground - Platform"][0].top
            if arcade.check_for_collision(
                self.player, self.scene["Sewer door right - Interactive"][-1]
            ):
                new_position = self.scene["Sewer ground - Platform"][0].top
            for ladder in self.scene["Ladder right - Interactive"]:
                if arcade.check_for_collision(self.player, ladder):
                    new_position = self.scene["Concrete ground - Platform"][0].top

            if new_position is not None:
                self.player.position = self.player.center_x, new_position + self.player.height // 2

            self.e_pressed = False
            self.camera.position = self.player.position # type: ignore

        if self.left_pressed and not self.right_pressed:
            if self.player.character_facing_direction == RIGHT_FACING:
                self.player.turn()

            self.player.current_animation = "walk"

        elif self.right_pressed and not self.left_pressed:
            if self.player.character_facing_direction == LEFT_FACING:
                self.player.turn()

            self.player.current_animation = "walk"

        # Stop the player if no key is being pressed
        else:
            self.player.current_animation = "idle"

    def on_update(
            self,
            delta_time: float
        ) -> None:

        self.player.update(delta_time)
        self.soldiers.update(delta_time, banjo=self.player)

        self.handle_player_controls()

        self.camera.position = self.player.position # type: ignore

    def on_key_press(
            self,
            symbol: int,
            modifiers: int
        ) -> None:

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
        elif symbol == arcade.key.E:
            self.e_pressed = True
        elif symbol == arcade.key.F:
            self.set_fullscreen(fullscreen=not self.fullscreen)
            self.set_vsync(vsync=True)

    def on_key_release(
            self,
            symbol: int,
            modifiers: int
        ) -> None:

        if symbol == arcade.key.LEFT:
            self.left_pressed = False
        elif symbol == arcade.key.RIGHT:
            self.right_pressed = False
        elif symbol == arcade.key.M:
            self.m_pressed = False
        elif symbol == arcade.key.B:
            self.b_pressed = False

    def on_resize(
            self,
            width: int,
            height: int
        ) -> None:

        # Call the parent. Failing to do this will mess up the coordinates,
        # and default to 0,0 at the center and the edges being -1 to 1.
        super().on_resize(width, height)
        self.camera.match_window()