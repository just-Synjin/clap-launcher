from src.audio_capture import AudioCapture
from src.clap_detector import ClapDetector
from src.launcher import GameLauncher
from src.config import load_config


detector = ClapDetector()
config = load_config()
launcher = GameLauncher(game_path=config["game_path"])

def handle_window(rms, sf):
    result = detector.process(rms, sf)
    if result:
        launcher.launch()

capture = AudioCapture(on_window=handle_window)
capture.start()
