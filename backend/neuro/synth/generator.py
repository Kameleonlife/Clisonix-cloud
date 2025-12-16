import numpy as np

class ToneSynth:
    def generate_layers(self, duration, freqs, valence, arousal, tempo):
        sr = 44100
        t = np.linspace(0, duration, int(sr*duration))

        output = np.zeros_like(t)

        # dynamics
        amplitude = 0.3 + 0.3*valence
        vibrato = 0.005 * arousal

        for f in freqs:
            signal = amplitude * np.sin(2*np.pi*f*t + vibrato*np.sin(2*np.pi*5*t))
            output += signal

        # apply simple rhythmic pulse
        rhythm = np.sin(2*np.pi*(tempo/60.0)*t)
        output *= (0.5 + 0.5*rhythm)

        # normalize
        output /= np.max(np.abs(output)) + 1e-9

        return output

