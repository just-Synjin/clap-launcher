# Clap Launcher

A background utility that listens to your microphone and launches a Steam game when it detects two claps in a row.

## How it works

The detector combines two audio features to reliably distinguish a clap from speech or background noise:

- **RMS (loudness)** — compared against an adaptive background threshold that continuously recalibrates to the current noise floor.
- **Spectral flatness** — measures how "broadband" the sound is. A clap produces a noise-like, broadband spectrum, while voice is concentrated around a fundamental tone and its harmonics.

A small state machine handles debouncing, so a single clap's echo/reverberation isn't mistaken for a second clap. After a successful double-clap, detection pauses for about 40 seconds before listening again, to prevent accidental re-triggers.

## Requirements

- Windows
- Steam, with the target game installed
- [uv](https://docs.astral.sh/uv/) for dependency management (only needed if running from source)

## Download

Grab the latest `ClapLauncher.exe` from the [Releases](../../releases) page — no Python installation required.

## Important: disable microphone enhancements

Windows and audio drivers (e.g. Realtek) often apply noise suppression / voice enhancement to your microphone by default. These filters are specifically designed to suppress sharp, broadband impulsive sounds — which unfortunately includes claps, breaking detection.

**Before using this app**, disable microphone enhancements:

`Control Panel → Sound → Recording → (your microphone) → Properties → Enhancements tab` — uncheck everything (Noise Suppression, Echo Cancellation, etc.), or disable equivalent options in your audio card's control panel (Realtek Audio Console, Nahimic, etc.).

## Usage

1. Run `ClapLauncher.exe`.
2. On first run, a settings window opens — enter the **Steam App ID** of the game you want to launch (found in the game's store URL: `store.steampowered.com/app/<ID>/...`).
3. The app minimizes to the system tray and listens in the background.
4. Clap twice within about 1.3 seconds to launch the game via Steam.
5. After a successful trigger, detection pauses for ~40 seconds before listening again.
6. Right-click the tray icon:
   - **Settings** — change the configured Steam App ID at any time.
   - **Quit** — close the app.

## Running from source

```bash
git clone <repo-url>
cd clap-launcher
uv sync
uv run main.py
```

## Building the executable yourself

```bash
uv add pyinstaller --dev
uv run pyinstaller --onefile --windowed --name ClapLauncher main.py
```

The resulting `.exe` will be in `dist/`.

## Project structure

```
clap-launcher/
├── main.py               # entry point — wires everything together
├── config.json            # stores the configured Steam App ID (created on first run)
├── src/
│   ├── audio_capture.py   # microphone capture, sliding window RMS + spectral flatness
│   ├── clap_detector.py   # state machine + adaptive threshold clap detection
│   ├── launcher.py        # launches the game via steam://run/<appid>
│   ├── gui.py              # tkinter settings window (Steam App ID input)
│   ├── tray.py              # system tray icon, Settings/Quit menu, background threading
│   └── config.py            # config.json read/write helpers
```

## Known limitations

- Detection thresholds (`sf_threshold`, cooldown durations, wait timeout) were tuned on a specific microphone and room; you may need to adjust them in `src/clap_detector.py` if detection feels too sensitive or not sensitive enough.
- Only tested on Windows, with microphone enhancements disabled.
- Requires Steam to be installed and the game to already be in your library.