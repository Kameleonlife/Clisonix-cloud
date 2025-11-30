import librosa
import numpy as np

class HPSEngine:
    def __init__(self):
        pass

    def scan(self, audio_path: str) -> dict:
        y, sr = librosa.load(audio_path, sr=None)

        # ----------------------------------------------------
        # 1) Tonalitet (Key Detection)
        # ----------------------------------------------------
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        chroma_mean = chroma.mean(axis=1)
        key_index = np.argmax(chroma_mean)

        key = self._key_from_index(key_index)

        # ----------------------------------------------------
        # 2) Tempo (BPM)
        # ----------------------------------------------------
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        # ----------------------------------------------------
        # 3) Harmonic Fingerprint
        # ----------------------------------------------------
        harmonic, percussive = librosa.effects.hpss(y)
        spectral_centroid = librosa.feature.spectral_centroid(y=harmonic, sr=sr).mean()

        # ----------------------------------------------------
        # 4) Emotional Tone (Valence + Arousal)
        # ----------------------------------------------------
        valence = float((spectral_centroid / 8000))  # 0–1
        arousal = float(tempo / 200)                 # 0–1

        emotion = self._emotion_from_values(valence, arousal)

        # ----------------------------------------------------
        # 5) Personality Archetype
        # ----------------------------------------------------
        archetype = self._archetype_from_emotion(emotion)

        return {
            "key": key,
            "tempo_bpm": float(tempo),
            "spectral_centroid": float(spectral_centroid),
            "valence": valence,
            "arousal": arousal,
            "emotion": emotion,
            "archetype": archetype
        }

    def _key_from_index(self, idx: int) -> str:
        KEYS = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
        return KEYS[idx % 12]

    def _emotion_from_values(self, v, a):
        if v > 0.6 and a > 0.6:
            return "energetic_happy"
        if v > 0.6 and a < 0.4:
            return "calm_positive"
        if v < 0.4 and a > 0.6:
            return "tense"
        if v < 0.4 and a < 0.4:
            return "sad"
        return "neutral"

    def _archetype_from_emotion(self, e):
        mapping = {
            "energetic_happy": "The Flame",
            "calm_positive": "The Ocean",
            "tense": "The Warrior",
            "sad": "The Dreamer",
            "neutral": "The Architect",
        }
        return mapping.get(e, "The Signal")
