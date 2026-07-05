import numpy as np
import sounddevice as sd

class AudioCapture:
    def __init__(self, semplerate=44100, blocksize=1024, buffersize=4096, windowsize=1024, step=441):
        self.semplerate = semplerate
        self.blocksize = blocksize
        self.buffersize = buffersize
        self.buffer = np.zeros(buffersize)
        self.windowsize = windowsize
        self.step = step

    def _update_buffer(self, new_block):
        self.buffer[:-self.blocksize] = self.buffer[self.blocksize:]
        self.buffer[-self.blocksize:] = new_block

    def _extract_window(self):
        for i in range(0, self.buffersize - self.windowsize + 1, self.step):
            window = self.buffer[i: i + self.windowsize]
            rms = np.sqrt(np.mean(window**2))
            print(f"Window [{i}:{i + self.windowsize}] | RMS: {rms:.4f}")

    def _callback(self, indata, frames, time, status):
        mono_block = np.mean(indata, axis=1)
        self._update_buffer(mono_block)
        self._extract_window()

    def start(self):
        try:
            with sd.InputStream(samplerate=self.semplerate, blocksize=self.blocksize, callback=self._callback):
                while True: sd.sleep(1000)

        except KeyboardInterrupt:
            print("Stop!")
