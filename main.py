from src.audio_capture import AudioCapture
from src.clap_detector import ClapDetector
from src.launcher import GameLauncher
from src.config import load_config
from src.gui import main as run_gui
from src.tray import run_tray
import threading

config = load_config()

if not config.get("steam_appid"):
    print("Steam App ID not configured, opening settings window...")
    run_gui()
    config = load_config()

detector = ClapDetector()
launcher = GameLauncher(steam_appid=config["steam_appid"])

def handle_window(rms, sf):
    result = detector.process(rms, sf)
    if result:
        launcher.launch()

def open_settings():
    run_gui()
    new_config = load_config()
    launcher.steam_appid = new_config.get("steam_appid", "")

capture = AudioCapture(on_window=handle_window)
thread = threading.Thread(target=capture.start, daemon=True)
thread.start()

run_tray(on_quit=lambda: None, on_settings=open_settings)