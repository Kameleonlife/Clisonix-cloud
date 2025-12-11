"""
Audio to MIDI converter
Stub implementation - requires librosa/aubio for production
"""
import tempfile


class AudioToMidi:
    """Converts audio files to MIDI"""
    
    def convert(self, audio_path: str, midi_path: str) -> str:
        """
        Convert audio file to MIDI
        
        Args:
            audio_path: Path to input audio file
            midi_path: Path to output MIDI file
            
        Returns:
            Path to generated MIDI file
        """
        # TODO: Implement with librosa pitch detection + pretty_midi
        # For now, return a stub path
        return midi_path
