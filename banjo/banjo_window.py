from __future__ import annotations

__all__ = ["GameWindow"]

import arcade
from banjo.characters import Banjo, Soldier1, Soldier2, Soldier3
import math
import random

# Constants
# 720p is the resolution of the game
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SCALE = 1.5
SCREEN_TITLE = "Banjo"
SOLDIER = Soldier1
GRAVITY_ACCELERATION = -981


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

        # Player controller variables
        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.m_pressed: bool = False
        self.b_pressed: bool = False
        self.d_pressed: bool = False
        self.e_pressed: bool = False

        # Interactive map elements
        self.garage_broken: bool = False

        self.physics_engine = arcade.PymunkPhysicsEngine()

    def setup(self) -> None:
        """Set up the game window.
        """
        # Initialize the player and NPC
        self.player = Banjo()
        self.soldiers: arcade.SpriteList = arcade.SpriteList()
        for _ in range(1):
            self.soldiers.append(Soldier1())

        # Set the initial position of the player and soldiers
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2

        offset = 400
        for soldier in self.soldiers:
            soldier.center_x = SCREEN_WIDTH // 2 + offset
            soldier.center_y = SCREEN_HEIGHT // 2
            soldier.set_path([2000])
            offset += 100

        # Set the initial position of the camera
        self.camera = arcade.Camera2D()

        # Load the map and set the scene
        tile_map = arcade.load_tilemap("./tiled/map.tmx", scaling=TILE_SCALE)
        self.scene = arcade.Scene.from_tilemap(tile_map)

        # Add Banjo to the scene and add his sprite
        # to the physics engine
        self.scene.add_sprite("Banjo", self.player)

        self.physics_engine.add_sprite(
            self.player,
            friction=self.player.friction,
            mass=self.player.mass,
            moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
            collision_type="player",
            gravity=(0, GRAVITY_ACCELERATION * self.player.mass),
            elasticity=0
        )

        # Add Soldier NPCs to the scene and add their sprites
        # to the physics engine
        for i, soldier in enumerate(self.soldiers):
            self.scene.add_sprite(f"BRAVO-[1-{i}]", soldier)

            self.physics_engine.add_sprite(
                soldier,
                friction=soldier.friction,
                mass=soldier.mass,
                moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
                collision_type="enemy",
                gravity=(0, GRAVITY_ACCELERATION * soldier.mass),
                elasticity=0
            )

        # Add the tilemap to the scene
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

    def handle_player_controls(self) -> None:
        """ Handle player controls.
        """
        # Cannot move the player if it is dead
        if self.player.is_dying:
            return

        # Maybe you want to die on command, I won't judge
        # It is not a bug, it is a feature >:)
        if self.d_pressed:
            self.player.current_animation = "death"
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
                self.physics_engine.set_position(
                    self.player,
                    (self.player.center_x, new_position + self.player.height / 2),
                )
            self.e_pressed = False
            self.camera.position = self.player.position # type: ignore

        if self.left_pressed and not self.right_pressed:
            if self.player.character_face_direction == 0:
                self.player.turn()

            self.player.current_animation = "walk"
            self.physics_engine.set_horizontal_velocity(self.player, -self.player.walking_velocity)

        elif self.right_pressed and not self.left_pressed:
            if self.player.character_face_direction == 1:
                self.player.turn()

            self.player.current_animation = "walk"
            self.physics_engine.set_horizontal_velocity(self.player, self.player.walking_velocity)

        # Stop the player if no key is being pressed
        else:
            self.physics_engine.set_horizontal_velocity(self.player, 0)
            self.player.current_animation = "idle"

    def soldier_face_banjo(
            self,
            soldier: SOLDIER
        ) -> None:
        """ Make the soldier face Banjo.

        Parameters
        ----------
        `soldier` : SOLDIER
            The soldier to check.
        """
        soldier.character_face_direction = 1 if self.player.center_x < soldier.center_x else 0

    def patrol_soldier(
            self,
            soldier: SOLDIER,
            delta_time: float
        ) -> None:
        """ Handle the patrol behavior of the soldiers.

        Parameters
        ----------
        `soldier` : SOLDIER
            The soldier to patrol.
        `delta_time` : float
            The time since the last update.
        """
        if soldier.current_animation == "alert":
            return

        # Overwrite the hurt animation if the soldier is hurt
        # and give it a delay before it can attack again via
        # distance to Banjo
        if soldier.current_animation in ["hurt"]:
            if soldier.time_since_last_hit > soldier.time_to_recover:
                soldier.current_animation = "idle"
                soldier.time_since_last_hit = 0.0
            soldier.time_since_last_hit += delta_time
            return

        # Every N seconds of idle after running out of places to patrol
        # add a new position to the list
        # N here is `soldier.patrol_pace` and can vary from soldier to soldier
        if not soldier.position_list:
            if soldier.time_since_last_coordinate > soldier.patrol_pace:
                soldier.time_since_last_coordinate = 0.0
                soldier.position_list.append(random.randint(0, SCREEN_WIDTH))
            soldier.time_since_last_coordinate += delta_time

            soldier.current_animation = "idle"
            self.physics_engine.set_horizontal_velocity(
                soldier,
                0
            )

            return

        target_x = soldier.position_list[0]

        if target_x < soldier.center_x:
            soldier.character_face_direction = 1
            soldier.current_animation = "walk"
            self.physics_engine.set_horizontal_velocity(
                soldier,
                -soldier.walking_velocity
            )

        elif target_x > soldier.center_x:
            soldier.character_face_direction = 0
            soldier.current_animation = "walk"
            self.physics_engine.set_horizontal_velocity(
                soldier,
                soldier.walking_velocity
            )

        # Stop the soldier if it is close enough to the target
        # This is to avoid the soldier getting stuck in a local
        # minimum from overshooting and looping forever
        if abs(soldier.center_x - target_x) < 5:
            soldier.position_list.pop(0)
            soldier.current_animation = "idle"
            self.physics_engine.set_horizontal_velocity(
                soldier,
                0
            )

    def can_see_banjo(
            self,
            soldier: SOLDIER
        ) -> tuple[bool, bool]:
        """ Check if the soldier can see Banjo. The code determines whether
        Banjo is within the soldier's melee and shooting range. The melee
        range is 100 pixels and the shooting range is defined by the soldier's
        range attribute.

        Parameters
        ----------
        `soldier` : SOLDIER
            The soldier to check.

        Returns
        -------
        `can_melee` : bool
            A boolean representing whether the soldier can melee Banjo.
        `can_shoot` : bool
            A boolean representing whether the soldier can shoot Banjo.
        """
        can_melee = False
        can_shoot = False

        if abs(self.player.center_y - soldier.center_y) > 50:
            return can_melee, can_shoot

        if soldier.character_face_direction == 0:
            if (
                self.player.center_x > soldier.center_x
                and abs(self.player.center_x - soldier.center_x) < soldier.range
            ):
                can_shoot = True

        else:
            if (
                self.player.center_x < soldier.center_x
                and abs(self.player.center_x - soldier.center_x) < soldier.range
            ):
                can_shoot = True

        if abs(self.player.center_x - soldier.center_x) < 100:
            can_melee = True

        return can_melee, can_shoot

    def can_hear_banjo(
            self,
            soldier: SOLDIER
        ) -> bool:
        """ Check if the soldier can hear Banjo. The code determines whether
        Banjo is within the soldier's hearing range. The hearing range is
        defined by the soldier's hearing_range attribute.

        Parameters
        ----------
        `soldier` : SOLDIER
            The soldier to check.

        Returns
        -------
        `can_hear` : bool
            A boolean representing whether the soldier can hear Banjo.
        """
        if abs(math.sqrt(
            (self.player.center_x - soldier.center_x) ** 2 +
            (self.player.center_y - soldier.center_y) ** 2
        )) < soldier.hearing_range:
            return True

        return False

    def chase_banjo(
            self,
            soldier: SOLDIER
        ) -> None:
        """ Handle the chasing of Banjo by the soldiers.

        Parameters
        ----------
        `soldier` : SOLDIER
            The soldier to check.
        """
        if self.player.position[0] > soldier.position[0]:
            banjo_anticipated_position = self.player.position[0] + soldier.range
        else:
            banjo_anticipated_position = self.player.position[0] - soldier.range

        soldier.position_list = [int(banjo_anticipated_position)] + soldier.position_list

    def shoot_banjo(
            self,
            soldier: SOLDIER
        ) -> None:
        """ Handle the shooting of Banjo by the soldiers.

        Parameters
        ----------
        `soldier` : SOLDIER
            The soldier to check.
        """
        if not self.can_see_banjo(soldier)[1]:
            return

        # Ensure the soldier does not shoot when he should be
        # melee attacking or being hurt
        if soldier.current_animation in ["melee", "hurt"]:
            return

        soldier.current_animation = "aim_fire"

        # Any contact with the player will trigger the chase process
        self.chase_banjo(soldier)

        self.soldier_face_banjo(soldier)
        self.physics_engine.set_horizontal_velocity(soldier, 0)

        # Check if the soldier hit Banjo
        if soldier.current_texture_index in soldier.shoot_impact_texture_indices:
            hit_chance = random.random()
            if hit_chance > soldier.accuracy:
                # self.player.damaged(soldier.attack)
                pass

    def melee_banjo(
            self,
            soldier: SOLDIER
        ) -> None:
        """ Handle the melee attack of the soldiers.

        Parameters
        ----------
        `soldier` : SOLDIER
            The soldier to check.
        """
        if not self.can_see_banjo(soldier)[0]:
            return

        # Ensure the soldier does not melee when he is hurt
        # to avoid the soldier being OP and spamming melee attacks
        # while being hurt
        if soldier.current_animation in ["alert", "hurt"]:
            return

        soldier.current_animation = "melee"

        # Any contact with the player will trigger the chase process
        self.chase_banjo(soldier)

        self.soldier_face_banjo(soldier)
        self.physics_engine.set_horizontal_velocity(soldier, 0)

        if soldier.current_texture_index in soldier.melee_impact_texture_indices:
            # self.player.damaged(soldier.attack)
            pass

    def melee_soldier(
            self,
            soldier: SOLDIER
        ) -> None:
        """ Handle the melee attack of Banjo on the soldiers.

        Parameters
        ----------
        `soldier` : SOLDIER
            The soldier to check.
        """
        if abs(self.player.center_x - soldier.center_x) < 100:
            if self.player.current_animation == "melee":
                # Explicitly set the soldier to hurt animation
                # to add a delay before the soldier can attack again
                # If soldier is hurt only in `soldier.damaged` then it
                # will never run the hurt animation due to it being overwritten
                # by the melee animation
                soldier.current_animation = "hurt"
                if self.player.current_texture_index in self.player.melee_impact_texture_indices:
                    # soldier.damaged(self.player.attack)
                    pass

    def banjo_bark(
            self,
            soldier: SOLDIER
        ) -> None:
        """ Handle the barking of Banjo.

        Parameters
        ----------
        `soldier` : SOLDIER
            The soldier to check.

        Returns
        -------
        `bark` : bool
            A boolean representing whether Banjo is barking.
        """
        if not self.player.current_animation == "bark":
            return

        if self.can_hear_banjo(soldier):
            soldier.current_animation = "alert"
            self.chase_banjo(soldier)

    def on_update(
            self,
            delta_time: float
        ) -> None:

        if self.player.is_dead:
            for soldier in self.soldiers:
                soldier.at_ease = True

        self.player.update_animation(delta_time)
        self.soldiers.update_animation(delta_time)

        self.handle_player_controls()

        for soldier in self.soldiers:
            self.patrol_soldier(soldier, delta_time)
            self.banjo_bark(soldier)
            self.melee_banjo(soldier)
            self.shoot_banjo(soldier)
            self.melee_soldier(soldier)

        self.camera.position = self.player.position # type: ignore

        self.physics_engine.step()

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