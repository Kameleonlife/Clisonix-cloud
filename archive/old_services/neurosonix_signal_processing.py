# -*- coding: utf-8 -*-
"""Advanced Neural Signal Processing Engine for Clisonix Industrial Platform"""

from __future__ import annotations

import numpy as np
import scipy.signal as sp
import scipy.stats as stats
import pywt
from typing import Iterable, List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import logging

from Clisonix_telemetry import trace, metrics

logger = logging.getLogger(__name__)

class SignalProcessingMode(Enum):
    REAL_TIME = "real_time"
    BATCH_PROCESSING = "batch_processing" 
    STREAMING = "streaming"
    OFFLINE_ANALYSIS = "offline_analysis"

class NeuralFrequencyBand(Enum):
    DELTA = (0.5, 4.0)
    THETA = (4.0, 8.0)
    ALPHA = (8.0, 13.0)
    BETA = (13.0, 30.0)
    GAMMA = (30.0, 100.0)
    HIGH_GAMMA = (100.0, 200.0)

@dataclass
class NeuralSignalConfig:
    sampling_rate: float = 1000.0  # Hz
    notch_frequency: float = 50.0  # Hz (power line noise)
    highpass_cutoff: float = 0.5   # Hz
    lowpass_cutoff: float = 200.0  # Hz
    wavelet_type: str = 'db4'
    segment_length: int = 1024
    overlap: float = 0.5

@dataclass
class ProcessingResult:
    processed_signal: np.ndarray
    frequency_bands: Dict[NeuralFrequencyBand, np.ndarray]
    time_frequency_representation: np.ndarray
    artifacts_detected: List[Artifact]
    signal_quality_metrics: SignalQualityMetrics
    feature_vectors: Dict[str, np.ndarray]

@dataclass
class Artifact:
    type: str  # 'ocular', 'muscle', 'line_noise', 'movement'
    start_index: int
    end_index: int
    confidence: float
    severity: float

@dataclass
class SignalQualityMetrics:
    snr_db: float
    artifact_ratio: float
    stationarity_score: float
    complexity_measure: float
    connectivity_patterns: np.ndarray

class NeuroSignalProcessor:
    """Advanced neural signal processing engine for EEG/ECoG/LFP signals"""
    
    def __init__(self, config: NeuralSignalConfig = None):
        self.config = config or NeuralSignalConfig()
        self._initialize_filters()
        self._initialize_wavelets()
        logger.info("NeuroSignalProcessor initialized with config: %s", self.config)
    
    def _initialize_filters(self):
        """Initialize digital filters for signal preprocessing"""
        # Notch filter for power line noise
        self.notch_b, self.notch_a = sp.iirnotch(
            self.config.notch_frequency, 
            30, 
            self.config.sampling_rate
        )
        
        # Bandpass filter for neural signals
        nyquist = self.config.sampling_rate / 2
        self.bandpass_b, self.bandpass_a = sp.butter(
            4, 
            [self.config.highpass_cutoff/nyquist, self.config.lowpass_cutoff/nyquist],
            btype='band'
        )
    
    def _initialize_wavelets(self):
        """Initialize wavelet transforms for time-frequency analysis"""
        self.wavelet = pywt.Wavelet(self.config.wavelet_type)
        self.scales = np.arange(1, 128)
    
    @trace
    @metrics.timer('signal.full_processing')
    def process_neural_signal(self, 
                            raw_signal: np.ndarray,
                            mode: SignalProcessingMode = SignalProcessingMode.REAL_TIME,
                            channel_info: Optional[Dict] = None) -> ProcessingResult:
        """
        Complete neural signal processing pipeline
        """
        logger.info("Starting neural signal processing for %d samples", len(raw_signal))
        
        # Step 1: Preprocessing and artifact removal
        cleaned_signal = self._preprocess_signal(raw_signal)
        
        # Step 2: Artifact detection and characterization
        artifacts = self._detect_artifacts(cleaned_signal)
        
        # Step 3: Frequency band decomposition
        frequency_bands = self._decompose_frequency_bands(cleaned_signal)
        
        # Step 4: Time-frequency analysis
        time_freq_repr = self._compute_time_frequency_representation(cleaned_signal)
        
        # Step 5: Feature extraction
        features = self._extract_features(cleaned_signal, frequency_bands, time_freq_repr)
        
        # Step 6: Signal quality assessment
        quality_metrics = self._assess_signal_quality(cleaned_signal, artifacts, features)
        
        result = ProcessingResult(
            processed_signal=cleaned_signal,
            frequency_bands=frequency_bands,
            time_frequency_representation=time_freq_repr,
            artifacts_detected=artifacts,
            signal_quality_metrics=quality_metrics,
            feature_vectors=features
        )
        
        logger.info("Signal processing completed. SNR: %.2f dB, Artifacts: %d", 
                   quality_metrics.snr_db, len(artifacts))
        
        return result
    
    @trace
    def _preprocess_signal(self, signal: np.ndarray) -> np.ndarray:
        """Comprehensive signal preprocessing pipeline"""
        # 1. Detrending
        detrended = sp.detrend(signal, type='linear')
        
        # 2. Notch filtering (power line noise)
        notch_filtered = sp.filtfilt(self.notch_b, self.notch_a, detrended)
        
        # 3. Bandpass filtering
        bandpass_filtered = sp.filtfilt(self.bandpass_b, self.bandpass_a, notch_filtered)
        
        # 4. Z-score normalization
        normalized = (bandpass_filtered - np.mean(bandpass_filtered)) / np.std(bandpass_filtered)
        
        return normalized
    
    @trace
    def _detect_artifacts(self, signal: np.ndarray) -> List[Artifact]:
        """Advanced artifact detection using multiple methods"""
        artifacts = []
        
        # 1. Detect high-amplitude artifacts (muscle, movement)
        amplitude_threshold = np.std(signal) * 5
        high_amp_indices = np.where(np.abs(signal) > amplitude_threshold)[0]
        
        if len(high_amp_indices) > 0:
            artifacts.append(Artifact(
                type='high_amplitude',
                start_index=high_amp_indices[0],
                end_index=high_amp_indices[-1],
                confidence=0.95,
                severity=np.mean(np.abs(signal[high_amp_indices])) / amplitude_threshold
            ))
        
        # 2. Detect line noise using FFT
        fft_signal = np.abs(np.fft.fft(signal))
        freqs = np.fft.fftfreq(len(signal), 1/self.config.sampling_rate)
        line_noise_idx = np.argmin(np.abs(freqs - self.config.notch_frequency))
        
        if fft_signal[line_noise_idx] > np.mean(fft_signal) * 10:
            artifacts.append(Artifact(
                type='line_noise',
                start_index=0,
                end_index=len(signal),
                confidence=0.8,
                severity=fft_signal[line_noise_idx] / np.mean(fft_signal)
            ))
        
        # 3. Detect non-stationarities
        stationarity_score = self._compute_stationarity(signal)
        if stationarity_score < 0.7:
            artifacts.append(Artifact(
                type='non_stationary',
                start_index=0,
                end_index=len(signal),
                confidence=0.7,
                severity=1 - stationarity_score
            ))
        
        return artifacts
    
    @trace
    def _decompose_frequency_bands(self, signal: np.ndarray) -> Dict[NeuralFrequencyBand, np.ndarray]:
        """Decompose signal into standard neural frequency bands"""
        bands = {}
        nyquist = self.config.sampling_rate / 2
        
        for band in NeuralFrequencyBand:
            low_freq, high_freq = band.value
            
            # Design bandpass filter for each frequency band
            b, a = sp.butter(4, [low_freq/nyquist, high_freq/nyquist], btype='band')
            band_signal = sp.filtfilt(b, a, signal)
            
            # Apply Hilbert transform to get envelope
            analytic_signal = sp.hilbert(band_signal)
            amplitude_envelope = np.abs(analytic_signal)
            
            bands[band] = amplitude_envelope
        
        return bands
    
    @trace
    def _compute_time_frequency_representation(self, signal: np.ndarray) -> np.ndarray:
        """Compute wavelet-based time-frequency representation"""
        coefficients, frequencies = pywt.cwt(
            signal, 
            self.scales, 
            self.wavelet, 
            sampling_period=1/self.config.sampling_rate
        )
        return np.abs(coefficients) ** 2  # Power spectrum
    
    @trace
    def _extract_features(self, 
                         signal: np.ndarray,
                         frequency_bands: Dict[NeuralFrequencyBand, np.ndarray],
                         time_freq_repr: np.ndarray) -> Dict[str, np.ndarray]:
        """Extract comprehensive feature set from processed signal"""
        features = {}
        
        # Time-domain features
        features['mean_amplitude'] = np.array([np.mean(signal)])
        features['std_amplitude'] = np.array([np.std(signal)])
        features['skewness'] = np.array([stats.skew(signal)])
        features['kurtosis'] = np.array([stats.kurtosis(signal)])
        
        # Frequency-domain features
        psd = np.abs(np.fft.fft(signal)) ** 2
        features['spectral_entropy'] = np.array([self._compute_spectral_entropy(psd)])
        
        # Band power features
        for band, band_signal in frequency_bands.items():
            features[f'{band.name.lower()}_power'] = np.array([np.mean(band_signal ** 2)])
        
        # Nonlinear features
        features['hurst_exponent'] = np.array([self._compute_hurst_exponent(signal)])
        features['sample_entropy'] = np.array([self._compute_sample_entropy(signal)])
        
        # Connectivity features (if multi-channel)
        if len(signal.shape) > 1 and signal.shape[1] > 1:
            features['functional_connectivity'] = self._compute_functional_connectivity(signal)
        
        return features
    
    @trace
    def _assess_signal_quality(self, 
                              signal: np.ndarray,
                              artifacts: List[Artifact],
                              features: Dict[str, np.ndarray]) -> SignalQualityMetrics:
        """Comprehensive signal quality assessment"""
        # Signal-to-Noise Ratio
        noise_floor = np.percentile(np.abs(signal), 10)
        signal_power = np.mean(signal ** 2)
        snr_db = 10 * np.log10(signal_power / (noise_floor ** 2 + 1e-10))
        
        # Artifact ratio
        total_artifact_samples = sum(art.end_index - art.start_index for art in artifacts)
        artifact_ratio = total_artifact_samples / len(signal)
        
        # Stationarity
        stationarity_score = self._compute_stationarity(signal)
        
        # Complexity measure
        complexity = self._compute_sample_entropy(signal)
        
        return SignalQualityMetrics(
            snr_db=snr_db,
            artifact_ratio=artifact_ratio,
            stationarity_score=stationarity_score,
            complexity_measure=complexity,
            connectivity_patterns=np.array([])  # Placeholder for multi-channel
        )
    
    def _compute_stationarity(self, signal: np.ndarray, window_size: int = 100) -> float:
        """Compute stationarity score using sliding window statistics"""
        if len(signal) < window_size * 2:
            return 1.0
        
        means, stds = [], []
        for i in range(0, len(signal) - window_size, window_size // 2):
            window = signal[i:i + window_size]
            means.append(np.mean(window))
            stds.append(np.std(window))
        
        # Stationarity score based on variance of statistics across windows
        mean_variation = np.std(means) / (np.std(signal) + 1e-10)
        std_variation = np.std(stds) / (np.std(signal) + 1e-10)
        
        return 1.0 - (mean_variation + std_variation) / 2
    
    def _compute_spectral_entropy(self, power_spectrum: np.ndarray) -> float:
        """Compute spectral entropy of the signal"""
        # Normalize power spectrum to probability distribution
        psd_norm = power_spectrum / np.sum(power_spectrum)
        psd_norm = psd_norm[psd_norm > 0]  # Remove zeros for log
        
        # Compute spectral entropy
        spectral_entropy = -np.sum(psd_norm * np.log(psd_norm))
        
        # Normalize by maximum possible entropy
        max_entropy = np.log(len(psd_norm))
        return spectral_entropy / max_entropy if max_entropy > 0 else 0
    
    def _compute_hurst_exponent(self, signal: np.ndarray) -> float:
        """Compute Hurst exponent for long-range dependence"""
        # Simplified rescaled range analysis
        n = len(signal)
        max_lag = min(n // 4, 100)
        
        r_s = []
        lags = range(2, max_lag)
        
        for lag in lags:
            # Rescaled range calculation
            segments = n // lag
            if segments < 2:
                continue
                
            r_s_lag = []
            for i in range(segments):
                segment = signal[i * lag:(i + 1) * lag]
                mean_segment = np.mean(segment)
                cumulative_deviation = np.cumsum(segment - mean_segment)
                r = np.max(cumulative_deviation) - np.min(cumulative_deviation)
                s = np.std(segment)
                if s > 0:
                    r_s_lag.append(r / s)
            
            if r_s_lag:
                r_s.append(np.mean(r_s_lag))
        
        if len(r_s) > 1:
            lags_array = np.array(lags[:len(r_s)])
            r_s_array = np.array(r_s)
            hurst, _ = np.polyfit(np.log(lags_array), np.log(r_s_array), 1)
            return hurst
        else:
            return 0.5  # Random walk
    
    def _compute_sample_entropy(self, signal: np.ndarray, m: int = 2, r: float = 0.2) -> float:
        """Compute sample entropy for complexity measurement"""
        # Simplified sample entropy calculation
        n = len(signal)
        if n < m + 1:
            return 0
        
        # Template vectors
        templates_m = np.array([signal[i:i + m] for i in range(n - m)])
        templates_m1 = np.array([signal[i:i + m + 1] for i in range(n - m - 1)])
        
        # Distance threshold
        r_val = r * np.std(signal)
        
        # Count matches
        matches_m = 0
        matches_m1 = 0
        
        for i in range(len(templates_m)):
            for j in range(i + 1, len(templates_m)):
                if np.max(np.abs(templates_m[i] - templates_m[j])) <= r_val:
                    matches_m += 1
                    if np.max(np.abs(templates_m1[i] - templates_m1[j])) <= r_val:
                        matches_m1 += 1
        
        if matches_m > 0 and matches_m1 > 0:
            return -np.log(matches_m1 / matches_m)
        else:
            return 0
    
    def _compute_functional_connectivity(self, multi_channel_signal: np.ndarray) -> np.ndarray:
        """Compute functional connectivity matrix for multi-channel signals"""
        n_channels = multi_channel_signal.shape[1]
        connectivity = np.zeros((n_channels, n_channels))
        
        for i in range(n_channels):
            for j in range(i + 1, n_channels):
                # Pearson correlation
                corr = np.corrcoef(multi_channel_signal[:, i], multi_channel_signal[:, j])[0, 1]
                connectivity[i, j] = corr
                connectivity[j, i] = corr
        
        np.fill_diagonal(connectivity, 1.0)
        return connectivity

# Advanced processing functions with telemetry
@trace
@metrics.timer('signal.multichannel_processing')
def process_multichannel_eeg(eeg_data: np.ndarray, 
                           sampling_rate: float = 1000.0,
                           channel_names: List[str] = None) -> Dict[str, ProcessingResult]:
    """Process multi-channel EEG data with channel-wise analysis"""
    processor = NeuroSignalProcessor(NeuralSignalConfig(sampling_rate=sampling_rate))
    results = {}
    
    for channel_idx in range(eeg_data.shape[1]):
        channel_signal = eeg_data[:, channel_idx]
        channel_name = channel_names[channel_idx] if channel_names else f"Channel_{channel_idx}"
        
        results[channel_name] = processor.process_neural_signal(
            channel_signal, 
            SignalProcessingMode.BATCH_PROCESSING
        )
    
    return results

@trace  
@metrics.timer('signal.real_time_processing')
def real_time_neural_monitoring(signal_buffer: np.ndarray,
                              config: NeuralSignalConfig) -> ProcessingResult:
    """Real-time neural signal processing for monitoring applications"""
    processor = NeuroSignalProcessor(config)
    return processor.process_neural_signal(
        signal_buffer, 
        SignalProcessingMode.REAL_TIME
    )

if __name__ == "__main__":
    # Demo with synthetic multi-channel EEG data
    print("ðŸ§  Clisonix Advanced Neural Signal Processing Engine")
    print("=" * 60)
    
    # Generate synthetic EEG data
    time = np.linspace(0, 10, 10000)  # 10 seconds at 1000 Hz
    n_channels = 8
    
    # Create synthetic multi-channel EEG with different rhythms
    eeg_data = np.zeros((len(time), n_channels))
    
    for ch in range(n_channels):
        # Mix of different neural rhythms
        delta = 0.5 * np.sin(2 * np.pi * 2 * time)  # Delta waves
        alpha = 0.3 * np.sin(2 * np.pi * 10 * time + ch)  # Alpha waves
        beta = 0.2 * np.sin(2 * np.pi * 20 * time + ch * 2)  # Beta waves
        noise = 0.1 * np.random.randn(len(time))  # Background noise
        
        eeg_data[:, ch] = delta + alpha + beta + noise
    
    # Process all channels
    channel_names = [f"EEG_{i}" for i in range(n_channels)]
    results = process_multichannel_eeg(eeg_data, 1000.0, channel_names)
    
    print(f"âœ… Processed {n_channels} EEG channels")
    
    # Display results for first channel
    first_channel = list(results.values())[0]
    print(f"ðŸ“Š Signal Quality Metrics:")
    print(f"   SNR: {first_channel.signal_quality_metrics.snr_db:.2f} dB")
    print(f"   Artifact Ratio: {first_channel.signal_quality_metrics.artifact_ratio:.3f}")
    print(f"   Stationarity: {first_channel.signal_quality_metrics.stationarity_score:.3f}")
    print(f"   Complexity: {first_channel.signal_quality_metrics.complexity_measure:.3f}")
    
    print(f"ðŸŽ¯ Detected {len(first_channel.artifacts_detected)} artifacts")
    print(f"ðŸ“ˆ Extracted {len(first_channel.feature_vectors)} feature types")
    print(f"ðŸŒŠ Frequency bands analyzed: {list(first_channel.frequency_bands.keys())}")