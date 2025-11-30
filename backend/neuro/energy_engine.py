import librosa
import numpy as np
from backend.neuro.brainsync_engine import BrainSyncEngine

class EnergyEngine:

    def __init__(self):
        self.sync = BrainSyncEngine()

    def analyze(self, audio_path: str):
        y, sr = librosa.load(audio_path, sr=None)

        # 1. Pitch & dominant frequency
        f0, voiced, probs = librosa.pyin(
            y, 
            fmin=float(librosa.note_to_hz('C2')),
            fmax=float(librosa.note_to_hz('C7'))
        )
        dominant_freq = float(np.nanmean(f0))

        # 2. Vocal tension (jitter + shimmer)
        jitter = float(np.nanstd(np.diff(f0)) if np.nanstd(np.diff(f0)) == np.nanstd(np.diff(f0)) else 0)
        shimmer = float(np.std(y[:20000]))

        # 3. Spectral centroid → brightness (mood)
        centroid = float(librosa.feature.spectral_centroid(y=y, sr=sr).mean())

        # 4. Energy Score (0–100)
        energy_score = int(np.clip((centroid / 5000) * 100, 0, 100))

        # 5. Emotion mapping
        emotion = self._emotion(centroid, jitter)

        # 6. Quick sound recommendation
        sound_file = self.sync.generate(
            mode=self._mode_from_emotion(emotion),
            profile={
                "key": "A",
                "tempo_bpm": 70,
                "valence": centroid / 8000,
                "arousal": energy_score / 100
            }
        )

        return {
            "dominant_frequency": dominant_freq,
            "vocal_tension": float(jitter),
            "brightness_centroid": centroid,
            "energy_score": energy_score,
            "emotion": emotion,
            "recommendation_sound": sound_file
        }

    def _emotion(self, centroid, jitter):
        if centroid > 3500 and jitter < 10:
            return "energized"
        if centroid < 2000 and jitter < 15:
            return "calm"
        if jitter > 25:
            return "stressed"
        if centroid < 1500:
            return "tired"
        return "neutral"

    def _mode_from_emotion(self, emotion):
        MAP = {
            "energized": "motivation",
            "calm": "relax",
            "stressed": "recovery",
            "tired": "sleep",
            "neutral": "relax"
        }
        return MAP.get(emotion, "relax")
