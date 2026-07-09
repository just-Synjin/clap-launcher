from src.audio_capture import AudioCapture
from src.clap_detector import ClapDetector


detector = ClapDetector()

def handle_window(rms, sf):
    result = detector.process(rms, sf)
    if result:
        print("Clap handled! Launching game")

capture = AudioCapture(on_window=handle_window)
capture.start()
