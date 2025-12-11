import sys
sys.path.append('/path/to/your/project/root')

import numpy as np
from .vision.color_analysis import ColorAnalyzer # type: ignore
from backend.neuro.hps_engine import HPSEngine
from backend.neuro.brainsync_engine import BrainSyncEngine

class MoodboardEngine:

    def __init__(self):
        self.color = ColorAnalyzer()
        self.hps = HPSEngine()
        self.sync = BrainSyncEngine()

    def generate(self, text=None, mood=None, file_path=None):
        # ---------------------------
        # 1. EMOTION BASED ON TEXT
        # ---------------------------
        text_emotion = None
        if text:
            text_emotion = self._text_to_emotion(text)

        # ---------------------------
        # 2. COLOR EXTRACTION (IMAGE)
        # ---------------------------
        dom_color = None
        palette = None
        if file_path and self.color.is_image(file_path):
            dom_color, palette = self.color.extract(file_path)

        # ---------------------------
        # 3. HARMONICS (AUDIO)
        # ---------------------------
        audio_hps = None
        if file_path and self.color.is_audio(file_path):
            audio_hps = self.hps.scan(file_path)

        # ---------------------------
        # 4. MOOD SELECTION
        # ---------------------------
        final_mood = mood or text_emotion or "neutral"

        # ---------------------------
        # 5. MINI SOUND (10 sec)
        # ---------------------------
        short_sound_path = self.sync.generate(
            mode=self._mood_to_mode(final_mood),
            profile=audio_hps or {
                "key": "A",
                "tempo_bpm": 80,
                "valence": 0.5,
                "arousal": 0.5
            }
        )

        # ---------------------------
        # 6. QUOTE GENERATION (STATIC)
        # (can be replaced with your ASI generator)
        # ---------------------------
        quote = self._quote(final_mood)

        return {
            "mood": final_mood,
            "color_dominant": dom_color,
            "palette": palette,
            "text_emotion": text_emotion,
            "sound_profile": audio_hps,
            "quote": quote,
            "sound_file": short_sound_path
        }

    # Helpers ----------------------------------------

    def _text_to_emotion(self, text):
        text = text.lower()
        if any(w in text for w in ["sad", "lonely", "hurt"]):
            return "sad"
        if any(w in text for w in ["happy", "joy", "love"]):
            return "happy"
        if any(w in text for w in ["focus", "work", "study"]):
            return "focus"
        if any(w in text for w in ["calm", "peace", "relax"]):
            return "calm"
        return "neutral"

    def _mood_to_mode(self, mood):
        MAP = {
            "happy": "motivation",
            "sad": "recovery",
            "focus": "focus",
            "calm": "relax",
            "dreamy": "creativity",
            "energetic": "motivation",
            "neutral": "relax",
        }
        return MAP.get(mood, "relax")

    def _quote(self, mood):
        Q = {
            "happy": "Let the light inside you shine louder than any sound.",
            "sad": "Even quiet hearts have powerful rhythms.",
            "focus": "One thought. One wave. One path.",
            "calm": "Peace begins with your internal frequency.",
            "dreamy": "Imagination is your hidden symphony.",
            "energetic": "Your energy is your signature chord.",
            "neutral": "Balance is the music of clarity."
        }
        return Q.get(mood, "Find your frequency.")
