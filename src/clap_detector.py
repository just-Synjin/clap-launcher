import numpy as np
import time
from enum import Enum

class State(Enum):
    IDLE = 1
    COOLDOWN_1 = 2
    WAITING_SECOND = 3
    COOLDOWN_2 = 4

class ClapDetector():
    def __init__(self, rms_threshold=0.003, sf_threshold=0.5, cooldown_1_duration=0.2, cooldown_2_duration=0.2, wait_timeout=1.3):
        self.state = State.IDLE
        self.rms_threshold = rms_threshold
        self.sf_threshold = sf_threshold
        self.cooldown_1_duration = cooldown_1_duration
        self.cooldown_2_duration = cooldown_2_duration
        self.wait_timeout = wait_timeout
        self.state_entered_at = None

    def _is_clap(self, rms, sf):
        return (rms > self.rms_threshold) and (sf > self.sf_threshold)

    def process(self, rms, sf):
        """ Double-clap detector based on RMS (loudness) and spectral flatness (broadband nature).
    Uses a state machine: IDLE -> COOLDOWN_1 -> WAITING_SECOND -> COOLDOWN_2 -> IDLE.
    Cooldowns are necessary to avoid confusing the reverberation or echo of a single clap with a new event."""

        current_time = time.time()
        # state_entered_at is still None while we are in IDLE — guarding against a subtraction error
        time_in_state = (current_time - self.state_entered_at) if self.state_entered_at is not None else None

        if self.state == State.IDLE:
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
                self.state = State.IDLE
                return True
