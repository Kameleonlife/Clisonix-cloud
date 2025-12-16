"""
Fitness Module Database Models
Personalized fitness training, biometric tracking, and AI coaching
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List, Dict, Any
from sqlalchemy import Column, String, Float, Integer, DateTime, Text, Boolean, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()


class FitnessLevel(str, Enum):
    """User fitness level"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    ELITE = "elite"


class FitnessGoal(str, Enum):
    """User fitness goals"""
    WEIGHT_LOSS = "weight_loss"
    MUSCLE_GAIN = "muscle_gain"
    ENDURANCE = "endurance"
    STRENGTH = "strength"
    FLEXIBILITY = "flexibility"
    GENERAL_HEALTH = "general_health"
    SPORTS_PERFORMANCE = "sports_performance"


class ExerciseType(str, Enum):
    """Type of exercise"""
    CARDIO = "cardio"
    STRENGTH = "strength"
    FLEXIBILITY = "flexibility"
    BALANCE = "balance"
    SPORTS = "sports"
    RECOVERY = "recovery"


class WorkoutIntensity(str, Enum):
    """Workout intensity level"""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    HIIT = "hiit"


class BiometricType(str, Enum):
    """Type of biometric data"""
    HEART_RATE = "heart_rate"
    CALORIES_BURNED = "calories_burned"
    STEPS = "steps"
    DISTANCE = "distance"
    ELEVATION = "elevation"
    RESPIRATION_RATE = "respiration_rate"
    BLOOD_PRESSURE_SYSTOLIC = "blood_pressure_systolic"
    BLOOD_PRESSURE_DIASTOLIC = "blood_pressure_diastolic"
    OXYGEN_SATURATION = "oxygen_saturation"
    BODY_TEMPERATURE = "body_temperature"
    EMOTIONAL_STATE = "emotional_state"
    STRESS_LEVEL = "stress_level"
    SLEEP_QUALITY = "sleep_quality"
    FATIGUE = "fatigue"


class FitnessUser(Base):
    """User profile for fitness training"""
    __tablename__ = "fitness_users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    
    # Personal info
    age = Column(Integer, nullable=True)
    gender = Column(String(20), nullable=True)
    height_cm = Column(Float, nullable=True)  # Height in centimeters
    weight_kg = Column(Float, nullable=True)  # Weight in kilograms
    
    # Fitness profile
    fitness_level = Column(SQLEnum(FitnessLevel), default=FitnessLevel.BEGINNER)
    primary_goal = Column(SQLEnum(FitnessGoal), nullable=True)
    secondary_goals = Column(JSON, default=list)  # List of FitnessGoal values
    
    # Biometric baseline (resting values)
    resting_heart_rate = Column(Float, nullable=True)  # BPM
    max_heart_rate = Column(Float, nullable=True)  # BPM (estimated if not set)
    vo2_max = Column(Float, nullable=True)  # ml/kg/min
    
    # Preferences
    preferred_workout_time = Column(String(50), nullable=True)  # "morning", "afternoon", "evening"
    preferred_intensity = Column(SQLEnum(WorkoutIntensity), default=WorkoutIntensity.MODERATE)
    workout_duration_minutes = Column(Integer, default=45)
    workouts_per_week = Column(Integer, default=3)
    
    # Wearables integration
    linked_wearables = Column(JSON, default=dict)  # {"device_type": "device_id"}
    camera_enabled = Column(Boolean, default=False)  # For emotion detection
    microphone_enabled = Column(Boolean, default=False)  # For audio coaching
    
    # Metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    last_login = Column(DateTime, nullable=True)
    active = Column(Boolean, default=True)
    
    # Relationships
    workouts = relationship("Workout", back_populates="user", cascade="all, delete-orphan")
    biometrics = relationship("BiometricData", back_populates="user", cascade="all, delete-orphan")
    coaching_sessions = relationship("CoachingSession", back_populates="user", cascade="all, delete-orphan")
    achievements = relationship("UserAchievement", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<FitnessUser(id={self.id}, username={self.username}, goal={self.primary_goal})>"


class Workout(Base):
    """Workout session record"""
    __tablename__ = "workouts"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("fitness_users.id"), nullable=False, index=True)
    
    # Workout details
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    workout_type = Column(SQLEnum(ExerciseType), nullable=False)
    intensity = Column(SQLEnum(WorkoutIntensity), default=WorkoutIntensity.MODERATE)
    
    # Timing
    started_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    
    # Performance metrics
    total_calories_burned = Column(Float, default=0.0)
    average_heart_rate = Column(Float, nullable=True)
    max_heart_rate = Column(Float, nullable=True)
    min_heart_rate = Column(Float, nullable=True)
    total_steps = Column(Integer, default=0)
    distance_km = Column(Float, default=0.0)
    elevation_m = Column(Float, default=0.0)
    
    # Emotional/Physical state
    mood_before = Column(String(20), nullable=True)  # "excellent", "good", "neutral", "tired", "stressed"
    mood_after = Column(String(20), nullable=True)
    energy_before = Column(Integer, nullable=True)  # 1-10 scale
    energy_after = Column(Integer, nullable=True)
    pain_level = Column(Integer, nullable=True)  # 0-10 scale
    
    # Music/Audio
    music_playlist_id = Column(String(255), nullable=True)
    adaptive_music_bpm = Column(Integer, nullable=True)  # Beats per minute of adaptive music
    motivational_cues = Column(JSON, default=list)  # Audio coaching messages
    
    # AI Coaching
    form_corrections = Column(JSON, default=list)  # List of form correction events
    ai_feedback = Column(Text, nullable=True)  # Overall AI coaching feedback
    
    # Metadata
    completed = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    weather_conditions = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    user = relationship("FitnessUser", back_populates="workouts")
    exercises = relationship("Exercise", back_populates="workout", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Workout(id={self.id}, user_id={self.user_id}, type={self.workout_type})>"


class Exercise(Base):
    """Individual exercise within a workout"""
    __tablename__ = "exercises"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workout_id = Column(String(36), ForeignKey("workouts.id"), nullable=False, index=True)
    
    # Exercise info
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    exercise_type = Column(SQLEnum(ExerciseType), nullable=False)
    muscle_groups = Column(JSON, default=list)  # ["chest", "triceps", "shoulders"]
    
    # Performance
    sets = Column(Integer, nullable=True)
    reps = Column(Integer, nullable=True)
    weight_kg = Column(Float, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    distance_m = Column(Float, nullable=True)
    
    # Form analysis
    form_score = Column(Float, default=0.0)  # 0-100 scale
    form_issues = Column(JSON, default=list)  # List of detected form problems
    recommended_form_corrections = Column(JSON, default=list)
    pose_detection_data = Column(JSON, nullable=True)  # MediaPipe output
    
    # AI Coaching feedback
    audio_coaching = Column(Text, nullable=True)  # Coaching message for this exercise
    difficulty_rating = Column(Integer, nullable=True)  # 1-10 scale
    
    # Metadata
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    workout = relationship("Workout", back_populates="exercises")
    
    def __repr__(self):
        return f"<Exercise(id={self.id}, name={self.name}, type={self.exercise_type})>"


class BiometricData(Base):
    """Real-time biometric measurements"""
    __tablename__ = "biometric_data"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("fitness_users.id"), nullable=False, index=True)
    
    # Measurement details
    biometric_type = Column(SQLEnum(BiometricType), nullable=False, index=True)
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)  # "bpm", "kcal", "mmHg", "%", etc.
    
    # Context
    measurement_time = Column(DateTime, nullable=False, index=True)
    context = Column(String(50), nullable=True)  # "rest", "workout", "recovery", "sleep"
    device_type = Column(String(50), nullable=True)  # "phone", "smartwatch", "chest_strap", etc.
    device_id = Column(String(255), nullable=True)
    
    # Additional data
    confidence_score = Column(Float, default=1.0)  # 0-1 scale
    raw_data = Column(JSON, nullable=True)  # Additional sensor data
    
    # Metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    user = relationship("FitnessUser", back_populates="biometrics")
    
    def __repr__(self):
        return f"<BiometricData(type={self.biometric_type}, value={self.value}, time={self.measurement_time})>"


class CoachingSession(Base):
    """AI Coaching session record"""
    __tablename__ = "coaching_sessions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("fitness_users.id"), nullable=False, index=True)
    
    # Session details
    session_type = Column(String(50), nullable=False)  # "form_correction", "motivation", "recovery", "nutrition"
    duration_seconds = Column(Integer, nullable=True)
    
    # Coaching content
    coaching_prompt = Column(Text, nullable=True)  # What was asked/what triggered coaching
    coaching_response = Column(Text, nullable=True)  # AI response/recommendation
    audio_guidance = Column(String(255), nullable=True)  # Path to audio file
    
    # Effectiveness
    user_feedback = Column(String(20), nullable=True)  # "helpful", "not_helpful", "neutral"
    effectiveness_score = Column(Float, default=0.0)  # 0-100 scale
    
    # Context
    exercise_id = Column(String(36), ForeignKey("exercises.id"), nullable=True)
    context_data = Column(JSON, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    user = relationship("FitnessUser", back_populates="coaching_sessions")
    
    def __repr__(self):
        return f"<CoachingSession(id={self.id}, type={self.session_type}, effectiveness={self.effectiveness_score})>"


class UserAchievement(Base):
    """Fitness achievements and milestones"""
    __tablename__ = "user_achievements"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("fitness_users.id"), nullable=False, index=True)
    
    # Achievement details
    achievement_type = Column(String(50), nullable=False)  # "milestone", "streak", "pr", "badge"
    achievement_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(255), nullable=True)  # URL to achievement icon
    
    # Value/Progress
    value = Column(Float, nullable=True)  # e.g., 100 for "100 workouts completed"
    progress = Column(Float, default=0.0)  # 0-100 scale
    
    # Metadata
    unlocked_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable=True)  # For time-limited achievements
    
    # Relationships
    user = relationship("FitnessUser", back_populates="achievements")
    
    def __repr__(self):
        return f"<UserAchievement(id={self.id}, name={self.achievement_name}, value={self.value})>"


class FitnessStats(Base):
    """Aggregated fitness statistics (for quick access)"""
    __tablename__ = "fitness_stats"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), unique=True, nullable=False, index=True)
    
    # Workout statistics
    total_workouts = Column(Integer, default=0)
    total_workout_hours = Column(Float, default=0.0)
    total_calories_burned = Column(Float, default=0.0)
    total_distance_km = Column(Float, default=0.0)
    total_steps = Column(Integer, default=0)
    
    # Streaks
    current_workout_streak = Column(Integer, default=0)
    longest_workout_streak = Column(Integer, default=0)
    current_workout_streak_started = Column(DateTime, nullable=True)
    
    # Averages
    avg_workout_duration_minutes = Column(Float, default=0.0)
    avg_heart_rate = Column(Float, default=0.0)
    avg_calories_per_workout = Column(Float, default=0.0)
    
    # Personal records
    max_heart_rate_recorded = Column(Float, default=0.0)
    longest_workout_minutes = Column(Integer, default=0)
    fastest_mile_seconds = Column(Integer, default=0)
    
    # Improvement metrics
    weekly_improvement_percent = Column(Float, default=0.0)
    monthly_improvement_percent = Column(Float, default=0.0)
    form_accuracy_trend = Column(Float, default=0.0)  # -100 to +100
    
    # Last updated
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"<FitnessStats(user_id={self.user_id}, total_workouts={self.total_workouts})>"


