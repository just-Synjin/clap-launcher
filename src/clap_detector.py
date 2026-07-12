import time
from enum import Enum

class State(Enum):
    IDLE = 1
    COOLDOWN_1 = 2
    WAITING_SECOND = 3
    COOLDOWN_2 = 4
    POST_TRIGGER_COOLDOWN = 5

class ClapDetector():
    def __init__(self, sf_threshold=0.5, cooldown_1_duration=0.2, cooldown_2_duration=0.2,
                 wait_timeout=1.3, post_trigger_cooldown_duration=40.0):
        self.state = State.IDLE
        self.sf_threshold = sf_threshold
        self.cooldown_1_duration = cooldown_1_duration
        self.cooldown_2_duration = cooldown_2_duration
        self.wait_timeout = wait_timeout
        self.post_trigger_cooldown_duration = post_trigger_cooldown_duration
        self.state_entered_at = None
        self.bg_mean = 0.0002
        self.bg_mean_sq = 0.0002 ** 2
        self.alpha = 0.05
        self.k = 10

    def _update_background(self, rms):
        if rms < self.bg_mean * 3:
            self.bg_mean = (1 - self.alpha) * self.bg_mean + self.alpha * rms
            self.bg_mean_sq = (1 - self.alpha) * self.bg_mean_sq + self.alpha * (rms ** 2)

    def _is_clap(self, rms, sf):
        variance = max(self.bg_mean_sq - self.bg_mean ** 2, 0)
        std = variance ** 0.5
        threshold = self.bg_mean + self.k * std
        return (rms > threshold) and (sf > self.sf_threshold)

    def process(self, rms, sf):
        current_time = time.time()
        time_in_state = (current_time - self.state_entered_at) if self.state_entered_at is not None else None

        if self.state == State.IDLE:
            self._update_background(rms)
            if self._is_clap(rms, sf):
                self.state = State.COOLDOWN_1
                self.state_entered_at = current_time

        elif self.state == State.COOLDOWN_1:
            if time_in_state > self.cooldown_1_duration:
                self.state = State.WAITING_SECOND
                self.state_entered_at = current_time

        elif self.state == State.WAITING_SECOND:
            if time_in_state > self.wait_timeout:
                self.state = State.IDLE
            elif self._is_clap(rms, sf):
                self.state = State.COOLDOWN_2
                self.state_entered_at = current_time

        elif self.state == State.COOLDOWN_2:
            if time_in_state > self.cooldown_2_duration:
                self.state = State.POST_TRIGGER_COOLDOWN
                self.state_entered_at = current_time
                return True

        elif self.state == State.POST_TRIGGER_COOLDOWN:
            if time_in_state > self.post_trigger_cooldown_duration:
                self.state = State.IDLE