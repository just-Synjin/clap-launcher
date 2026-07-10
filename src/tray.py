import threading
import pystray
from PIL import Image, ImageDraw

def create_icon_image():
    image = Image.new("RGB", (64, 64), "white")
    draw = ImageDraw.Draw(image)
    draw.ellipse((8, 8, 56, 56), fill="black")
    return image

def run_tray(on_quit):
    def quit_action(icon, item):
        icon.stop()
        on_quit()

    menu = pystray.Menu(
        pystray.MenuItem("Quit", quit_action)
    )

    icon = pystray.Icon("clap_launcher", create_icon_image(), "Clap Launcher", menu)
    icon.run()
