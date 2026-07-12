import os

class GameLauncher:
    def __init__(self, steam_appid):
        self.steam_appid = steam_appid

    def launch(self):
        if not self.steam_appid:
            print("Steam App ID not configured.")
            return False
        try:
            os.startfile(f"steam://run/{self.steam_appid}")
            return True
        except Exception as e:
            print(f"Launch error: {e}")
            return False