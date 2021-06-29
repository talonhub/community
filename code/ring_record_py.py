import os
import time

from talon_init import TALON_HOME
from talon import Module
from talon.microphone import manager as mic_manager
from talon.lib import cubeb, flac

TARGET = TALON_HOME / 'ring_record'
os.makedirs(TARGET, exist_ok=True)
ctx = cubeb.Context()

class RingRecord:
    def __init__(self, seconds):
        self.ring = [0] * 16000 * seconds
        self.pos = 0
        self.end = 0
        mic_manager.register('mic_change', self.start_stream)
        self.stream = None
        self.start_stream(mic_manager.active_mic())

    def start_stream(self, mic):
        if self.stream is None or mic != self.mic:
            if self.stream is not None:
                self.stream.stop()
                self.stream = None
            if mic is not None:
                input_params = cubeb.StreamParams(format=cubeb.SampleFormat.FLOAT32NE, rate=16000, channels=1)
                self.stream = ctx.new_input_stream("stream", mic, input_params,
                    latency=200, data_cb=self.on_data)
                self.stream.start()
        self.mic = mic 

    def on_data(self, stream, samples, _):
        remain = min(len(self.ring) - self.pos, len(samples))
        overflow = max(0, min(len(self.ring) - remain, len(samples) - remain))
        (
            self.ring[self.pos:self.pos+remain],
            self.ring[0:overflow],
            self.end,
            self.pos,
        ) = (
            samples[:remain],
            samples[remain:],
            max(self.end, min(self.pos + len(samples), len(self.ring))),
            (self.pos + len(samples)) % len(self.ring)
        )

recorder = RingRecord(seconds=5 * 60)

mod = Module()
@mod.action_class
class Actions:
    def ring_save():
        "Save audio ring buffer to file"
        n = int(time.time() * 1000)
        path = TARGET / f"{n}.flac"
        pos, end = recorder.pos, recorder.end
        samples = recorder.ring[pos:end] + recorder.ring[:pos]
        print(f"saving [audio]={len(samples) / 16000}s path={path}")
        flac.write_file(str(path), samples, compression_level=1, sample_rate=16000)
