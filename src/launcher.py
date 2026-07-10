import subprocess
import os

class GameLauncher:
    def __init__(self, game_path):
        self.game_path = game_path

    def launch(self):
        if not os.path.exists(self.game_path):
            print(f"File not found: {self.game_path}")
            return False

        try:
            subprocess.Popen(self.game_path)
            return True
        except Exception as e:
            print(f"Launch error: {e}")
            return False
