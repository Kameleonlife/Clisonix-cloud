"""
AI Coaching Engine
Real-time form correction, exercise recognition, and personalized coaching feedback
Uses pose estimation (MediaPipe) and biometric data
"""

import math
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime, timezone
import json

@dataclass
class FormAnalysis:
    """Pose/form analysis result"""
    exercise_name: str
    form_score: float  # 0-100
    issues: List[str]
    recommendations: List[str]
    timestamp: datetime


class CoachingEngine:
    """AI coaching system for real-time form correction and motivation"""
    
    # Ideal pose landmarks for common exercises
    EXERCISE_POSES = {
        "push_up": {
            "muscle_groups": ["chest", "triceps", "shoulders"],
            "duration_seconds": 2,
            "key_joints": ["shoulder", "elbow", "hip", "spine"],
            "ideal_angles": {
                "elbow": (60, 120),  # degrees
                "shoulder": (80, 120),
                "hip": (160, 180),  # Should be straight
                "spine": (0, 30)  # Minimal sag
            }
        },
        "squat": {
            "muscle_groups": ["quadriceps", "glutes", "hamstrings"],
            "duration_seconds": 3,
            "key_joints": ["hip", "knee", "ankle", "spine"],
            "ideal_angles": {
                "knee": (60, 100),  # 90 degrees ideal
                "hip": (60, 100),
                "ankle": (90, 110),
                "spine": (0, 20)  # Minimal forward lean
            }
        },
        "plank": {
            "muscle_groups": ["core", "chest", "shoulders"],
            "duration_seconds": 5,
            "key_joints": ["shoulder", "hip", "knee", "spine"],
            "ideal_angles": {
                "elbow": (160, 180),  # Should be straight
                "hip": (170, 180),  # Straight line
                "spine": (0, 15),  # Minimal sag
                "shoulder": (90, 100)  # Stacked over hands
            }
        },
        "deadlift": {
            "muscle_groups": ["back", "glutes", "hamstrings"],
            "duration_seconds": 3,
            "key_joints": ["hip", "knee", "spine", "shoulder"],
            "ideal_angles": {
                "knee": (40, 80),
                "hip": (30, 60),
                "spine": (0, 30),  # Neutral spine
                "shoulder": (75, 95)
            }
        },
        "bicep_curl": {
            "muscle_groups": ["biceps"],
            "duration_seconds": 2,
            "key_joints": ["elbow", "shoulder", "wrist"],
            "ideal_angles": {
                "elbow": (30, 160),  # Full range of motion
                "shoulder": (0, 30),  # Minimal movement
                "wrist": (80, 100)  # Neutral
            }
        },
        "pull_up": {
            "muscle_groups": ["back", "biceps"],
            "duration_seconds": 3,
            "key_joints": ["shoulder", "elbow", "hip", "knee"],
            "ideal_angles": {
                "elbow": (20, 160),  # Full range
                "shoulder": (80, 130),
                "hip": (160, 180),  # Straight legs
                "knee": (170, 180)
            }
        },
        "lunge": {
            "muscle_groups": ["quadriceps", "glutes", "hamstrings"],
            "duration_seconds": 3,
            "key_joints": ["hip", "knee", "ankle", "spine"],
            "ideal_angles": {
                "front_knee": (80, 110),
                "back_knee": (60, 90),
                "front_hip": (80, 110),
                "spine": (0, 15)
            }
        }
    }
    
    def __init__(self):
        self.session_feedback = []
        self.user_issues = {}  # Track recurring issues
    
    def analyze_pose(self, 
                    exercise_name: str,
                    pose_landmarks: Dict[str, Any],
                    confidence_scores: Dict[str, float]) -> FormAnalysis:
        """
        Analyze pose/form for an exercise
        
        pose_landmarks: {
            "shoulder": {"x": 0.5, "y": 0.3, "z": 0.0},
            "elbow": {"x": 0.6, "y": 0.4, "z": 0.1},
            ...
        }
        confidence_scores: {"shoulder": 0.95, "elbow": 0.92, ...}
        """
        
        exercise_name_lower = exercise_name.lower()
        
        if exercise_name_lower not in self.EXERCISE_POSES:
            return FormAnalysis(
                exercise_name=exercise_name,
                form_score=0.0,
                issues=["Exercise not recognized"],
                recommendations=["Add this exercise to the database"],
                timestamp=datetime.now(timezone.utc)
            )
        
        exercise_spec = self.EXERCISE_POSES[exercise_name_lower]
        issues = []
        form_score = 100.0
        
        # Filter landmarks by confidence
        filtered_landmarks = {
            k: v for k, v in pose_landmarks.items()
            if confidence_scores.get(k, 0) > 0.7
        }
        
        # Check for missing critical joints
        for joint in exercise_spec["key_joints"]:
            if joint not in filtered_landmarks:
                issues.append(f"Cannot detect {joint} - ensure proper camera angle")
                form_score -= 15
        
        if not filtered_landmarks:
            return FormAnalysis(
                exercise_name=exercise_name,
                form_score=0.0,
                issues=issues + ["Insufficient pose detection"],
                recommendations=["Move closer to camera", "Ensure proper lighting"],
                timestamp=datetime.now(timezone.utc)
            )
        
        # Analyze angles
        for angle_name, (min_deg, max_deg) in exercise_spec["ideal_angles"].items():
            angle = self._calculate_angle(angle_name, filtered_landmarks)
            
            if angle is None:
                continue
            
            if angle < min_deg - 10:
                issues.append(f"{angle_name} too closed ({angle:.0f}° vs ideal {min_deg}-{max_deg}°)")
                form_score -= 10
            elif angle > max_deg + 10:
                issues.append(f"{angle_name} too open ({angle:.0f}° vs ideal {min_deg}-{max_deg}°)")
                form_score -= 10
            elif angle < min_deg or angle > max_deg:
                form_score -= 5
        
        # Check body alignment
        alignment_issues = self._check_alignment(exercise_name_lower, filtered_landmarks)
        issues.extend(alignment_issues)
        form_score -= len(alignment_issues) * 3
        
        # Check symmetry
        symmetry_issues = self._check_symmetry(exercise_name_lower, filtered_landmarks)
        issues.extend(symmetry_issues)
        form_score -= len(symmetry_issues) * 5
        
        form_score = max(0, min(100, form_score))
        
        # Generate recommendations
        recommendations = self._generate_recommendations(exercise_name_lower, issues)
        
        # Track recurring issues
        if issues:
            if exercise_name_lower not in self.user_issues:
                self.user_issues[exercise_name_lower] = {}
            for issue in issues:
                self.user_issues[exercise_name_lower][issue] = self.user_issues[exercise_name_lower].get(issue, 0) + 1
        
        return FormAnalysis(
            exercise_name=exercise_name,
            form_score=form_score,
            issues=issues,
            recommendations=recommendations,
            timestamp=datetime.now(timezone.utc)
        )
    
    def _calculate_angle(self, angle_name: str, landmarks: Dict) -> Optional[float]:
        """Calculate angle between joints"""
        
        # Map angle names to joint sequences (joint1 -> joint2 -> joint3)
        angle_joints = {
            "elbow": ("shoulder", "elbow", "wrist"),
            "shoulder": ("hip", "shoulder", "elbow"),
            "hip": ("shoulder", "hip", "knee"),
            "knee": ("hip", "knee", "ankle"),
            "ankle": ("knee", "ankle", "foot"),
            "spine": ("neck", "hip", "shoulder"),
            "wrist": ("elbow", "wrist", "hand"),
            "front_knee": ("hip", "front_knee", "front_ankle"),
            "back_knee": ("hip", "back_knee", "back_ankle"),
            "front_hip": ("shoulder", "front_hip", "front_knee"),
        }
        
        if angle_name not in angle_joints:
            return None
        
        j1_name, j2_name, j3_name = angle_joints[angle_name]
        
        if j1_name not in landmarks or j2_name not in landmarks or j3_name not in landmarks:
            return None
        
        p1 = landmarks[j1_name]
        p2 = landmarks[j2_name]
        p3 = landmarks[j3_name]
        
        # Vector from p2 to p1
        v1 = (p1.get("x", 0) - p2.get("x", 0), p1.get("y", 0) - p2.get("y", 0), p1.get("z", 0) - p2.get("z", 0))
        # Vector from p2 to p3
        v2 = (p3.get("x", 0) - p2.get("x", 0), p3.get("y", 0) - p2.get("y", 0), p3.get("z", 0) - p2.get("z", 0))
        
        # Dot product
        dot_product = sum(a * b for a, b in zip(v1, v2))
        
        # Magnitudes
        mag1 = math.sqrt(sum(a**2 for a in v1))
        mag2 = math.sqrt(sum(a**2 for a in v2))
        
        if mag1 == 0 or mag2 == 0:
            return None
        
        # Angle in radians
        cos_angle = dot_product / (mag1 * mag2)
        cos_angle = max(-1, min(1, cos_angle))  # Clamp to [-1, 1]
        angle_rad = math.acos(cos_angle)
        angle_deg = math.degrees(angle_rad)
        
        return angle_deg
    
    def _check_alignment(self, exercise: str, landmarks: Dict) -> List[str]:
        """Check body alignment for given exercise"""
        issues = []
        
        if exercise == "push_up":
            # Check for sagging hips
            hip_y = landmarks.get("hip", {}).get("y")
            shoulder_y = landmarks.get("shoulder", {}).get("y")
            
            if hip_y and shoulder_y and hip_y > shoulder_y + 0.1:  # Hip lower than shoulder
                issues.append("Hips sagging - engage core")
        
        elif exercise == "squat":
            # Check if knees are going over toes
            knee_x = landmarks.get("knee", {}).get("x")
            ankle_x = landmarks.get("ankle", {}).get("x")
            
            if knee_x and ankle_x and abs(knee_x - ankle_x) > 0.15:
                issues.append("Knees caving inward - keep them aligned")
            
            # Check for forward lean
            spine_x = landmarks.get("spine", {}).get("x")
            hip_x = landmarks.get("hip", {}).get("x")
            
            if spine_x and hip_x and abs(spine_x - hip_x) > 0.1:
                issues.append("Excessive forward lean - maintain upright posture")
        
        elif exercise == "deadlift":
            # Check for round back
            spine_curve = self._estimate_spine_curvature(landmarks)
            if spine_curve > 30:  # degrees
                issues.append("Rounded back detected - keep spine neutral")
            
            # Check if bar is over midfoot
            bar_distance = self._estimate_bar_distance(landmarks)
            if bar_distance and bar_distance > 0.15:
                issues.append("Bar too far from body - keep it over midfoot")
        
        return issues
    
    def _check_symmetry(self, exercise: str, landmarks: Dict) -> List[str]:
        """Check for symmetry issues (left vs right side)"""
        issues = []
        
        # Check left vs right shoulder height
        left_shoulder = landmarks.get("left_shoulder", {}).get("y")
        right_shoulder = landmarks.get("right_shoulder", {}).get("y")
        
        if left_shoulder and right_shoulder:
            if abs(left_shoulder - right_shoulder) > 0.1:
                issues.append("Shoulder asymmetry - maintain even posture")
        
        # Check left vs right hip height
        left_hip = landmarks.get("left_hip", {}).get("y")
        right_hip = landmarks.get("right_hip", {}).get("y")
        
        if left_hip and right_hip:
            if abs(left_hip - right_hip) > 0.1:
                issues.append("Hip asymmetry - keep hips level")
        
        return issues
    
    def _estimate_spine_curvature(self, landmarks: Dict) -> float:
        """Estimate spinal curvature from landmarks"""
        # Simplified: check angle at multiple spine points
        neck_y = landmarks.get("neck", {}).get("y", 0)
        shoulder_y = landmarks.get("shoulder", {}).get("y", 0)
        hip_y = landmarks.get("hip", {}).get("y", 0)
        
        if hip_y > shoulder_y > neck_y:
            return 5  # Good alignment
        else:
            return 30  # Poor alignment
    
    def _estimate_bar_distance(self, landmarks: Dict) -> Optional[float]:
        """Estimate distance from body to bar (for deadlift)"""
        # Simplified: distance from hip to wrist
        hip_x = landmarks.get("hip", {}).get("x")
        wrist_x = landmarks.get("wrist", {}).get("x")
        
        if hip_x and wrist_x:
            return abs(hip_x - wrist_x)
        return None
    
    def _generate_recommendations(self, exercise: str, issues: List[str]) -> List[str]:
        """Generate personalized coaching recommendations"""
        recommendations = []
        
        base_recommendations = {
            "push_up": [
                "Engage your core to prevent hip sagging",
                "Keep elbows at ~45° from your body",
                "Maintain a straight line from head to heels",
                "Lower until chest nearly touches ground"
            ],
            "squat": [
                "Keep your chest upright",
                "Knees should track over toes",
                "Descend until thighs are parallel to ground",
                "Drive through heels to stand up"
            ],
            "deadlift": [
                "Keep bar over midfoot throughout",
                "Maintain neutral spine - no rounding",
                "Shoulders should be over the bar at start",
                "Drive hips forward powerfully"
            ],
            "pull_up": [
                "Use a full range of motion",
                "Engage your lats, not just arms",
                "Keep your body straight - no swinging",
                "Pull elbows down and back"
            ]
        }
        
        # Add base recommendations
        if exercise in base_recommendations:
            recommendations.extend(base_recommendations[exercise][:2])
        
        # Add issue-specific corrections
        if "hips sagging" in " ".join(issues).lower():
            recommendations.append("🔥 Core activation: Try planks or hollow holds to strengthen")
        if "rounded back" in " ".join(issues).lower():
            recommendations.append("🔥 Mobility work: Perform cat-cow stretches and thoracic extensions")
        if "knees caving" in " ".join(issues).lower():
            recommendations.append("🔥 Activation: Do lateral band walks before squats")
        if "shoulder asymmetry" in " ".join(issues).lower():
            recommendations.append("🔥 Balance work: Include single-arm exercises")
        
        return recommendations[:3]  # Return top 3 recommendations
    
    def generate_audio_coaching(self, 
                               exercise: str,
                               form_score: float,
                               heart_rate: Optional[float] = None,
                               emotional_state: Optional[str] = None) -> str:
        """Generate motivational audio coaching message"""
        
        messages = {
            "excellent": [
                "Perfect form! You're doing amazing!",
                "That's it! Textbook technique!",
                "Excellent form! Keep it up!"
            ],
            "good": [
                "Good work! You're nailing this!",
                "Nice effort! Maintain that form!",
                "Great technique! You got this!"
            ],
            "moderate": [
                "You're doing well! Focus on form!",
                "Good effort! Let's tighten up the form!",
                "Nice work! Keep pushing!"
            ],
            "needs_improvement": [
                "Let's dial in the form! You can do better!",
                "Focus on your technique! You've got this!",
                "Great effort! Let's correct the form!"
            ]
        }
        
        if form_score >= 85:
            category = "excellent"
        elif form_score >= 70:
            category = "good"
        elif form_score >= 50:
            category = "moderate"
        else:
            category = "needs_improvement"
        
        base_message = messages[category][hash(exercise) % 3]
        
        # Add heart rate coaching
        if heart_rate:
            if heart_rate > 160:
                base_message += " Pace yourself! Breathe!"
            elif heart_rate < 80:
                base_message += " Let's increase intensity!"
        
        # Add emotional state coaching
        if emotional_state == "stressed":
            base_message += " Stay calm and focus on your breathing!"
        elif emotional_state == "fatigued":
            base_message += " We're almost there! One more set!"
        
        return base_message
    
    def get_exercise_recognition_tips(self, exercise: str) -> Dict:
        """Get tips for better exercise recognition"""
        tips = {
            "push_up": [
                "Face camera at 45° angle",
                "Ensure entire body is in frame",
                "Good lighting from front and side",
                "No strong shadows on body"
            ],
            "squat": [
                "Stand facing camera directly",
                "Full body must be visible",
                "Position 5-8 feet from camera",
                "Minimal background clutter"
            ],
            "deadlift": [
                "Side view is best",
                "Ensure bar and body visible",
                "No shadows on spine",
                "Adequate space for full extension"
            ]
        }
        
        return {
            "exercise": exercise,
            "tips": tips.get(exercise, ["Ensure good camera angle", "Maintain proper lighting", "Full body visible"])
        }
    
    def get_recurring_issues(self, exercise: str) -> Dict:
        """Get recurring form issues for an exercise"""
        if exercise.lower() not in self.user_issues:
            return {
                "exercise": exercise,
                "recurring_issues": [],
                "total_attempts": 0
            }
        
        issues_data = self.user_issues[exercise.lower()]
        
        return {
            "exercise": exercise,
            "recurring_issues": sorted(
                [(issue, count) for issue, count in issues_data.items()],
                key=lambda x: x[1],
                reverse=True
            ),
            "total_attempts": sum(issues_data.values())
        }
