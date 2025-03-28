from banjo.soldier_window import GameWindow
# from banjo.soldier_2_window import GameWindow
# from banjo.game_window import GameWindow


if __name__ == "__main__":
    window = GameWindow()
    window.set_update_rate(1/10)
    window.setup()
    window.run()