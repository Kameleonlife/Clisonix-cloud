import numpy as np
import soundfile as sf
from backend.neuro.synth.generator import ToneSynth

class BrainSyncEngine:

    def __init__(self):
        self.synth = ToneSynth()

    def generate(self, mode: str, profile: dict) -> str:
        """
        mode: relax, focus, sleep, motivation, creativity, recovery
        profile: HPS result
        """

        key = profile["key"]
        tempo = profile["tempo_bpm"]
        valence = profile["valence"]
        arousal = profile["arousal"]

        # 1. Determine base frequency (key → Hz)
        base_freq = self._key_to_base_hz(key)

        # 2. Select brainwave target
        brain_freq = self._pick_brain_freq(mode)

        # 3. Build harmonics
        harmonics = [
            base_freq,
            base_freq * 2,
            base_freq * 3,
            brain_freq,          # brain-targeted
            7.83,                # Schumann resonance
        ]

        # 4. Generate audio
        signal = self.synth.generate_layers(
            duration=60,
            freqs=harmonics,
            valence=valence,
            arousal=arousal,
            tempo=tempo
        )

        out = "/tmp/brainsync_output.wav"
        sf.write(out, signal, 44100)
        return out

    def _pick_brain_freq(self, mode):
        mapping = {
            "relax": 8.0,       # alpha
            "focus": 14.0,      # high alpha/low beta
            "sleep": 2.0,       # delta
            "motivation": 12.0, # strong alpha
            "creativity": 10.0, # alpha-theta border
            "recovery": 7.83,   # schumann
        }
        return mapping.get(mode, 8.0)

    def _key_to_base_hz(self, key: str):
        MAP = {
            "C": 261.63, "C#": 277.18, "D": 293.66,
            "Eb": 311.13, "E": 329.63, "F": 349.23,
            "F#": 369.99, "G": 392.00, "Ab": 415.30,
            "A": 440.00, "Bb": 466.16, "B": 493.88
        }
        return MAP.get(key, 440.00)

