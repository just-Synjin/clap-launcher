import numpy as np
import sounddevice as sd

class AudioCapture:
    def __init__(self, semplerate=44100, blocksize=1024, buffersize=4096, windowsize=1024, step=441, on_window=None):
        self.semplerate = semplerate
        self.blocksize = blocksize
        self.buffersize = buffersize
        self.buffer = np.zeros(buffersize)
        self.windowsize = windowsize
        self.step = step
        self.on_window = on_window

    def _update_buffer(self, new_block):
        self.buffer[:-self.blocksize] = self.buffer[self.blocksize:]
        self.buffer[-self.blocksize:] = new_block

    def _spectral_flatness(self, window):
        epsilon = 1e-10

        spectrum = np.abs(np.fft.rfft(window))

        geometric_mean = np.exp(np.mean(np.log(spectrum + epsilon)))
        arithmetic_mean = np.mean(spectrum)

        return geometric_mean / (arithmetic_mean + epsilon)

    def _extract_window(self):
        for i in range(0, self.buffersize - self.windowsize + 1, self.step):
            window = self.buffer[i: i + self.windowsize]

            rms = np.sqrt(np.mean(window**2))
            sf = self._spectral_flatness(window)

        if self.on_window is not None:
            self.on_window(rms, sf)


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
