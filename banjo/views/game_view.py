from __future__ import annotations

__all__ = ["GameView"]

import arcade
from arcade.gui import UIView
from banjo.characters import Banjo, Soldier1, Platoon
from banjo.resources.game_constants import LEFT_FACING, RIGHT_FACING
from banjo.resources.level_maps import TILE_MAP, load_scene, load_platforms
import random


class GameView(UIView):
    """`banjo.views.GameView` is the class that represents the game view
    where the game is displayed. It is a subclass of `arcade.UIView` and
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
    `e_pressed` : bool
        A boolean representing whether the 'E' key is pressed.
    `player_died` : bool
        A boolean representing whether the player has died.
    `time_to_game_over` : float
        Add delay before the game over screen is displayed.
    `time_to_win` : float
        Add delay before the win screen is displayed.
    `garage_broken` : bool
        A boolean representing whether the garage door is broken.
    `player` : banjo.characters.Banjo
        The player character in the game.
    `soldiers` : banjo.characters.Platoon
        A platoon of soldier NPCs in the game. This is of type
        `arcade.SpriteList`.
    `camera` : arcade.Camera2D
        The camera used to render the game view.
    `scene` : arcade.Scene
        The scene containing all the sprites and interactive elements in the game.
    """
    def __init__(self) -> None:
        """ Initialize the game view.
        """
        super().__init__()

        arcade.set_background_color(arcade.color.BLACK)

        # Player controller variables
        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.m_pressed: bool = False
        self.b_pressed: bool = False
        self.d_pressed: bool = False
        self.e_pressed: bool = False

        # Game constants
        self.player_died: bool = False
        self.time_to_game_over: float = 0.0
        self.time_to_win: float = 0.0

        # Interactive map elements
        self.garage_broken: bool = False

    def setup(self) -> None:
        """Set up the game view.
        """
        # Load the map and set the scene
        # We need to create the scene and platforms here
        # to avoid snapshots of sprites when restarting
        # the view
        scene = load_scene(TILE_MAP)
        platforms = load_platforms(scene)

        for platform in platforms:
            platform.initialize()

        # Initialize the player and NPC
        self.player = Banjo()
        self.soldiers: Platoon = Platoon([Soldier1() for _ in range(3)])

        # Set the initial position of the player and soldiers
        self.player.center_x = 2400
        self.player.center_y = self.window.height // 2

        offset = 400
        for soldier in self.soldiers:
            soldier.center_x = self.window.width // 2 + offset
            soldier.center_y = self.window.height // 2
            soldier.fsm.set_patrol_checkpoints([random.randint(500, 2000)])
            offset += 100

        # Set the initial position of the camera
        self.camera = arcade.Camera2D()

        self.scene = scene

        # Add Banjo to the scene and add his sprite
        # to the physics engine
        self.scene.add_sprite("Banjo", self.player)

        # Add Soldier NPCs to the scene and add their sprites
        # to the physics engine
        for i, soldier in enumerate(self.soldiers):
            self.scene.add_sprite(f"BRAVO-[1-{i}]", soldier)

    def setup_hud(self) -> None:
        """ Set up the heads-up display (HUD) for the game view:
        - Draw the player's health bar.
        """
        bar_x = self.player.position[0]
        bar_y = self.player.position[1] + 60

        arcade.draw_lbwh_rectangle_filled(
            bar_x - 55,
            bar_y - 13,
            110,
            10,
            arcade.color.BLACK
        )

        # Smoothly interpolate the color based on HP
        if self.player.hp > self.player.max_hp * 0.65:
            color = arcade.color.GREEN
        elif self.player.hp > self.player.max_hp * 0.25:
            color = arcade.color.YELLOW
        else:
            color = arcade.color.RED

        arcade.draw_lbwh_rectangle_filled(
            bar_x - 50,
            bar_y - 10,
            100 * self.player.hp / self.player.max_hp,
            4,
            color
        )

    def check_end_level(self) -> bool:
        """ Check if the level has ended.

        Returns
        -------
        bool
            True if the level has ended, False otherwise.
        """
        for soldier in self.soldiers:
            if not soldier.current_state == "dead":
                return False
        return True

    def on_draw(self) -> None:
        self.clear()
        self.camera.use()
        self.scene.draw()
        self.setup_hud()

    def handle_player_controls(self) -> None:
        """ Handle player controls.
        """
        # Cannot move the player if it is dead
        if self.player.is_dying:
            self.player_died = True
            return

        # Maybe you want to die on command, I won't judge
        # It is not a bug, it is a feature >:)
        if self.d_pressed:
            self.player_died = True
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
            self.camera.position = self.player.position

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

        if self.player_died:
            self.time_to_game_over += delta_time
            if self.time_to_game_over > 5.0:
                self.game_over_screen()

        elif self.check_end_level():
            self.time_to_win += delta_time
            if self.time_to_win > 5.0:
                self.win_screen()

        self.player.update(delta_time)
        self.soldiers.update(delta_time, banjo=self.player)

        self.handle_player_controls()

        self.camera.position = self.player.position

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
        elif symbol == arcade.key.ESCAPE:
            from banjo.views import MidMenuView

            # Pause the game and show the mid menu
            self.window.show_view(MidMenuView(self))

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

        # Call the parent
        # Failing to do this will mess up the coordinates,
        # and default to 0,0 at the center and the edges
        # being -1 to 1
        super().on_resize(width, height)
        self.camera.match_window()

    def game_over_screen(self) -> None:
        """ Display the end screen.
        """
        from banjo.views import GameOverView

        self.window.show_view(GameOverView())

    def win_screen(self) -> None:
        """ Display the win screen.
        """
        from banjo.views import WinView

        self.window.show_view(WinView())