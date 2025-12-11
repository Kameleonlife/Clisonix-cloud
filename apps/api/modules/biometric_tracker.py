"""
Biometric Tracking Module
Real-time tracking of pulse, calories, emotional state, and other vital signs
Integrates with phone sensors and wearables
"""

import math
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import statistics

@dataclass
class BiometricReading:
    """Single biometric reading"""
    type: str  # "heart_rate", "calories", "emotional_state", etc.
    value: float
    timestamp: datetime
    device_type: str = "phone"  # "phone", "smartwatch", "chest_strap", etc.
    unit: str = ""  # "bpm", "kcal", "%", etc.
    confidence: float = 1.0  # 0-1 scale


class EmotionalState(str, Enum):
    """Detected emotional state from facial/pupil analysis"""
    RELAXED = "relaxed"
    CALM = "calm"
    NEUTRAL = "neutral"
    FOCUSED = "focused"
    ENGAGED = "engaged"
    STRESSED = "stressed"
    ANXIOUS = "anxious"
    FATIGUED = "fatigued"


class BiometricTracker:
    """Real-time biometric tracking system"""
    
    def __init__(self, user_id: str, user_profile: Dict):
        """
        Initialize tracker
        user_profile: {
            "age": 30,
            "weight_kg": 75,
            "height_cm": 180,
            "fitness_level": "intermediate",
            "resting_heart_rate": 60,
            "max_heart_rate": 190
        }
        """
        self.user_id = user_id
        self.user_profile = user_profile
        self.readings: List[BiometricReading] = []
        self.session_start: Optional[datetime] = None
        self.session_data = {
            "total_calories": 0.0,
            "max_heart_rate": 0,
            "min_heart_rate": 999,
            "avg_heart_rate": 0,
            "heart_rate_readings": [],
            "duration_seconds": 0,
            "emotional_states": [],
            "stress_levels": []
        }
    
    def start_session(self):
        """Start a tracking session (e.g., beginning a workout)"""
        self.session_start = datetime.now(timezone.utc)
        self.readings = []
        self.session_data = {
            "total_calories": 0.0,
            "max_heart_rate": 0,
            "min_heart_rate": 999,
            "avg_heart_rate": 0,
            "heart_rate_readings": [],
            "duration_seconds": 0,
            "emotional_states": [],
            "stress_levels": []
        }
        return {"status": "session_started", "timestamp": self.session_start}
    
    def end_session(self) -> Dict:
        """End tracking session and return summary"""
        if not self.session_start:
            return {"error": "No active session"}
        
        session_end = datetime.now(timezone.utc)
        duration = (session_end - self.session_start).total_seconds()
        self.session_data["duration_seconds"] = duration
        
        # Calculate averages
        if self.session_data["heart_rate_readings"]:
            self.session_data["avg_heart_rate"] = statistics.mean(self.session_data["heart_rate_readings"])
        
        # Finalize calories
        if self.session_data["duration_seconds"] > 0:
            avg_hr = self.session_data["avg_heart_rate"] or self.user_profile.get("resting_heart_rate", 60)
            self.session_data["total_calories"] = self._calculate_calories(
                duration_seconds=self.session_data["duration_seconds"],
                avg_heart_rate=avg_hr
            )
        
        self.session_start = None
        return {
            "status": "session_ended",
            "timestamp": session_end,
            "summary": self.session_data
        }
    
    def add_heart_rate_reading(self, bpm: float, device_type: str = "phone", timestamp: Optional[datetime] = None) -> BiometricReading:
        """Add heart rate reading (BPM)"""
        if timestamp is None:
            timestamp = datetime.now(timezone.utc)
        
        # Validate reading (typical range 40-200 BPM)
        if bpm < 40 or bpm > 200:
            bpm = max(40, min(200, bpm))  # Clamp to valid range
        
        reading = BiometricReading(
            type="heart_rate",
            value=bpm,
            timestamp=timestamp,
            device_type=device_type,
            unit="bpm"
        )
        
        self.readings.append(reading)
        
        if self.session_start:
            self.session_data["heart_rate_readings"].append(bpm)
            self.session_data["max_heart_rate"] = max(self.session_data["max_heart_rate"], bpm)
            self.session_data["min_heart_rate"] = min(self.session_data["min_heart_rate"], bpm)
        
        return reading
    
    def calculate_calories(self, heart_rate: float, duration_minutes: float) -> float:
        """
        Calculate calories burned using Karvonen formula
        Based on: (HR_reserve * intensity_factor + RHR) * duration
        """
        return self._calculate_calories(
            duration_seconds=duration_minutes * 60,
            avg_heart_rate=heart_rate
        )
    
    def _calculate_calories(self, duration_seconds: float, avg_heart_rate: float) -> float:
        """Internal calories calculation"""
        age = self.user_profile.get("age", 30)
        weight_kg = self.user_profile.get("weight_kg", 75)
        gender = self.user_profile.get("gender", "M")
        resting_hr = self.user_profile.get("resting_heart_rate", 60)
        
        duration_minutes = duration_seconds / 60.0
        
        # Karvonen formula: ((max HR - RHR) × %intensity / 100 + RHR) × 3.5 × weight
        # For simplification: (avg_HR - RHR) × duration_min × weight_factor
        hr_reserve = avg_heart_rate - resting_hr
        
        # Gender and age adjustment
        if gender.upper() == "M":
            calories_per_min = (hr_reserve * 0.02 + resting_hr * 0.001) * weight_kg / 75.0
        else:
            calories_per_min = (hr_reserve * 0.018 + resting_hr * 0.0009) * weight_kg / 65.0
        
        # Age adjustment (younger = slightly higher)
        age_factor = 1.0 + (40 - age) * 0.005
        calories_per_min *= age_factor
        
        total_calories = calories_per_min * duration_minutes
        return max(0, round(total_calories, 2))
    
    def detect_emotional_state(self, 
                              pupil_size: float,  # 0-10mm scale
                              pupil_dilation_rate: float,  # mm/sec
                              blink_rate: float,  # blinks per minute
                              eye_gaze_stability: float,  # 0-100 focus score
                              heart_rate: Optional[float] = None) -> Tuple[EmotionalState, float]:
        """
        Detect emotional state from pupil tracking and biometrics
        Returns: (emotional_state, confidence_score)
        """
        confidence = 0.0
        weights = {}
        
        # Pupil size analysis
        # Small pupils: relaxed, focused
        # Large pupils: interest, attention, or stress
        if pupil_size < 3.0:
            weights[EmotionalState.RELAXED] = 0.6
            weights[EmotionalState.CALM] = 0.5
        elif pupil_size < 5.0:
            weights[EmotionalState.NEUTRAL] = 0.6
            weights[EmotionalState.CALM] = 0.4
        elif pupil_size < 7.0:
            weights[EmotionalState.FOCUSED] = 0.7
            weights[EmotionalState.ENGAGED] = 0.5
        else:
            weights[EmotionalState.STRESSED] = 0.6
            weights[EmotionalState.ANXIOUS] = 0.5
        
        # Pupil dilation rate (rapid = stress/engagement)
        if abs(pupil_dilation_rate) > 0.5:
            weights[EmotionalState.STRESSED] = weights.get(EmotionalState.STRESSED, 0) + 0.4
            weights[EmotionalState.ENGAGED] = weights.get(EmotionalState.ENGAGED, 0) + 0.3
        elif abs(pupil_dilation_rate) < 0.1:
            weights[EmotionalState.RELAXED] = weights.get(EmotionalState.RELAXED, 0) + 0.3
        
        # Blink rate analysis
        # Normal: 15-20 blinks/min
        # High: stress, engagement
        # Low: focus, concentration
        if blink_rate < 10:
            weights[EmotionalState.FOCUSED] = weights.get(EmotionalState.FOCUSED, 0) + 0.5
            weights[EmotionalState.ENGAGED] = weights.get(EmotionalState.ENGAGED, 0) + 0.3
        elif blink_rate > 25:
            weights[EmotionalState.STRESSED] = weights.get(EmotionalState.STRESSED, 0) + 0.4
            weights[EmotionalState.ANXIOUS] = weights.get(EmotionalState.ANXIOUS, 0) + 0.3
        else:
            weights[EmotionalState.NEUTRAL] = weights.get(EmotionalState.NEUTRAL, 0) + 0.3
        
        # Gaze stability
        if eye_gaze_stability > 80:
            weights[EmotionalState.FOCUSED] = weights.get(EmotionalState.FOCUSED, 0) + 0.4
        elif eye_gaze_stability < 40:
            weights[EmotionalState.ANXIOUS] = weights.get(EmotionalState.ANXIOUS, 0) + 0.3
            weights[EmotionalState.STRESSED] = weights.get(EmotionalState.STRESSED, 0) + 0.2
        
        # Heart rate correlation
        if heart_rate:
            resting_hr = self.user_profile.get("resting_heart_rate", 60)
            max_hr = self.user_profile.get("max_heart_rate", 190)
            hr_percentage = ((heart_rate - resting_hr) / (max_hr - resting_hr)) * 100
            
            if hr_percentage < 30:
                weights[EmotionalState.CALM] = weights.get(EmotionalState.CALM, 0) + 0.3
            elif hr_percentage > 70:
                weights[EmotionalState.STRESSED] = weights.get(EmotionalState.STRESSED, 0) + 0.4
                weights[EmotionalState.ANXIOUS] = weights.get(EmotionalState.ANXIOUS, 0) + 0.2
        
        # Find dominant state
        if not weights:
            return (EmotionalState.NEUTRAL, 0.5)
        
        dominant_state = max(weights, key=weights.get)
        confidence = min(1.0, weights[dominant_state])
        
        # Record in session
        if self.session_start:
            self.session_data["emotional_states"].append({
                "state": dominant_state.value,
                "confidence": confidence,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
        
        # Record as reading
        reading = BiometricReading(
            type="emotional_state",
            value=confidence,
            timestamp=datetime.now(timezone.utc),
            device_type="camera",
            unit=""
        )
        self.readings.append(reading)
        
        return (dominant_state, confidence)
    
    def detect_stress_level(self, 
                           heart_rate: float,
                           heart_rate_variability: float,  # Standard deviation of HR intervals
                           pupil_dilation_rate: float,
                           respiratory_rate: Optional[float] = None) -> Tuple[int, str]:
        """
        Detect stress level (0-100 scale)
        Returns: (stress_level_0_100, interpretation)
        """
        stress_score = 0.0
        
        resting_hr = self.user_profile.get("resting_heart_rate", 60)
        max_hr = self.user_profile.get("max_heart_rate", 190)
        
        # Heart rate elevation (0-40 points)
        hr_percentage = ((heart_rate - resting_hr) / (max_hr - resting_hr)) * 100
        stress_score += min(40, max(0, hr_percentage * 0.4))
        
        # Heart rate variability (0-30 points)
        # Low HRV = stress, high HRV = relaxation
        if heart_rate_variability < 20:
            stress_score += 30
        elif heart_rate_variability < 50:
            stress_score += 20
        elif heart_rate_variability < 100:
            stress_score += 10
        
        # Pupil dilation (0-20 points)
        if abs(pupil_dilation_rate) > 0.5:
            stress_score += 20
        elif abs(pupil_dilation_rate) > 0.2:
            stress_score += 10
        
        # Respiratory rate (0-10 points) - elevated RR = stress
        if respiratory_rate:
            normal_rr = 12  # normal respiratory rate
            if respiratory_rate > 20:
                stress_score += 10
            elif respiratory_rate > 16:
                stress_score += 5
        
        stress_score = min(100, max(0, stress_score))
        
        # Interpretation
        if stress_score < 20:
            interpretation = "Very Relaxed"
        elif stress_score < 40:
            interpretation = "Relaxed"
        elif stress_score < 60:
            interpretation = "Normal"
        elif stress_score < 80:
            interpretation = "Stressed"
        else:
            interpretation = "Very Stressed"
        
        # Record in session
        if self.session_start:
            self.session_data["stress_levels"].append({
                "score": stress_score,
                "interpretation": interpretation,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
        
        return (int(stress_score), interpretation)
    
    def get_heart_rate_zones(self) -> Dict:
        """Get heart rate training zones"""
        max_hr = self.user_profile.get("max_heart_rate", 220 - self.user_profile.get("age", 30))
        
        return {
            "zone_1_warm_up": {
                "name": "Warm-up",
                "min_bpm": int(max_hr * 0.50),
                "max_bpm": int(max_hr * 0.60),
                "description": "Light activity, very easy"
            },
            "zone_2_aerobic": {
                "name": "Aerobic",
                "min_bpm": int(max_hr * 0.60),
                "max_bpm": int(max_hr * 0.70),
                "description": "Steady state, conversational"
            },
            "zone_3_tempo": {
                "name": "Tempo",
                "min_bpm": int(max_hr * 0.70),
                "max_bpm": int(max_hr * 0.80),
                "description": "Challenging, harder breathing"
            },
            "zone_4_threshold": {
                "name": "Threshold",
                "min_bpm": int(max_hr * 0.80),
                "max_bpm": int(max_hr * 0.90),
                "description": "Very hard, lactate threshold"
            },
            "zone_5_max": {
                "name": "Max Effort",
                "min_bpm": int(max_hr * 0.90),
                "max_bpm": int(max_hr),
                "description": "Maximum effort, sprint"
            }
        }
    
    def get_session_summary(self) -> Dict:
        """Get current session summary"""
        if not self.session_start:
            return {"status": "no_active_session"}
        
        duration = (datetime.now(timezone.utc) - self.session_start).total_seconds()
        
        return {
            "duration_seconds": duration,
            "total_calories": self.session_data["total_calories"],
            "heart_rate": {
                "current": self.session_data["heart_rate_readings"][-1] if self.session_data["heart_rate_readings"] else 0,
                "average": statistics.mean(self.session_data["heart_rate_readings"]) if self.session_data["heart_rate_readings"] else 0,
                "max": self.session_data["max_heart_rate"],
                "min": self.session_data["min_heart_rate"] if self.session_data["min_heart_rate"] != 999 else 0
            },
            "emotional_state": self.session_data["emotional_states"][-1] if self.session_data["emotional_states"] else None,
            "stress_level": self.session_data["stress_levels"][-1] if self.session_data["stress_levels"] else None,
            "readings_count": len(self.readings)
        }
    
    def get_all_readings(self, limit: Optional[int] = None) -> List[BiometricReading]:
        """Get all readings, optionally limited"""
        if limit:
            return self.readings[-limit:]
        return self.readings


# Demo/Testing Mode
if __name__ == "__main__":
    import time
    import random
    
    print("🧬 Biometric Tracker - Real-time Monitoring System")
    print("=" * 60)
    
    # Initialize with sample user profile
    user_profile = {
        "age": 30,
        "weight_kg": 75,
        "height_cm": 180,
        "fitness_level": "intermediate",
        "gender": "M",
        "resting_heart_rate": 60,
        "max_heart_rate": 190
    }
    
    tracker = BiometricTracker("user_001", user_profile)
    
    print(f"\n✓ Tracker initialized for user: user_001")
    print(f"  Age: {user_profile['age']}, Weight: {user_profile['weight_kg']}kg")
    print(f"  Resting HR: {user_profile['resting_heart_rate']} bpm")
    print(f"  Max HR: {user_profile['max_heart_rate']} bpm\n")
    
    # Start session
    print("📊 Starting monitoring session...")
    tracker.start_session()
    
    # Simulate real-time readings
    print("\n🔄 Simulating live biometric readings:\n")
    
    for i in range(10):
        # Simulate heart rate (60-120 bpm with variation)
        heart_rate = 70 + random.randint(-10, 30) + (i * 2)
        heart_rate = min(150, max(60, heart_rate))
        
        # Add heart rate reading
        reading = tracker.add_heart_rate_reading(heart_rate, device_type="smartwatch")
        print(f"  [{i+1}/10] ❤️  Heart Rate: {heart_rate} bpm | Time: {reading.timestamp.strftime('%H:%M:%S')}")
        
        # Detect emotional state every 3 readings
        if i % 3 == 0:
            pupil_size = 4.5 + random.uniform(-1, 1)
            pupil_dilation = random.uniform(-0.5, 0.5)
            blink_rate = 15 + random.randint(-5, 10)
            gaze_stability = 70 + random.randint(-20, 20)
            
            emotion, confidence = tracker.detect_emotional_state(
                pupil_size=pupil_size,
                pupil_dilation_rate=pupil_dilation,
                blink_rate=blink_rate,
                eye_gaze_stability=gaze_stability,
                heart_rate=heart_rate
            )
            print(f"    → Emotional State: {emotion.value} (confidence: {confidence:.2f})")
        
        # Detect stress level every 4 readings
        if i % 4 == 0:
            hrv = 50 + random.randint(-20, 30)
            pupil_dil = random.uniform(-0.3, 0.3)
            rr = 12 + random.randint(-2, 8)
            
            stress, interpretation = tracker.detect_stress_level(
                heart_rate=heart_rate,
                heart_rate_variability=hrv,
                pupil_dilation_rate=pupil_dil,
                respiratory_rate=rr
            )
            print(f"    → Stress Level: {stress}/100 ({interpretation})")
        
        time.sleep(0.5)
    
    # End session
    print("\n⏹️  Ending monitoring session...")
    summary = tracker.end_session()
    
    # Display results
    print("\n" + "=" * 60)
    print("📈 SESSION SUMMARY")
    print("=" * 60)
    
    session_summary = tracker.get_session_summary()
    if session_summary.get("status") != "no_active_session":
        print(f"\n✓ Session ended successfully")
        print(f"  Status: {summary['status']}")
        print(f"  Timestamp: {summary['timestamp']}")
    
    # Get heart rate zones
    zones = tracker.get_heart_rate_zones()
    print("\n💪 Heart Rate Training Zones:")
    for zone_name, zone_data in zones.items():
        print(f"  • {zone_data['name']:15} {zone_data['min_bpm']:3d}-{zone_data['max_bpm']:3d} bpm - {zone_data['description']}")
    
    # Show all readings
    all_readings = tracker.get_all_readings()
    print(f"\n📊 Total Readings Recorded: {len(all_readings)}")
    
    print("\n✅ Biometric Tracker demo completed successfully!")
    print("=" * 60)
