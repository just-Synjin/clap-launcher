from src.audio_capture import AudioCapture
from src.clap_detector import ClapDetector
from src.launcher import GameLauncher
from src.config import load_config
from src.gui import main as run_gui
from src.tray import run_tray
import threading

config = load_config()

if not config.get("game_path"):
    print("Game path not configured, opening settings window...")
    run_gui()
    config = load_config()  # re-read — in case the user saved a path

detector = ClapDetector()
launcher = GameLauncher(game_path=config["game_path"])

def handle_window(rms, sf):
    result = detector.process(rms, sf)
    if result:
        launcher.launch()

capture = AudioCapture(on_window=handle_window)

thread = threading.Thread(target=capture.start, daemon=True)
thread.start()

run_tray(on_quit=lambda:None)
