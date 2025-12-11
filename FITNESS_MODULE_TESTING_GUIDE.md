# Fitness Module - Testing Guide & Example Payloads

## 🧪 Complete Testing Workflow

This guide provides real-world payloads and workflows for testing all fitness module endpoints.

---

## Phase 1: User Profile Setup

### 1.1 Create User Profile
```bash
curl -X POST http://localhost:8000/fitness/users/profile \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice_fitness",
    "email": "alice@example.com",
    "age": 28,
    "gender": "F",
    "height_cm": 165,
    "weight_kg": 62,
    "fitness_level": "intermediate",
    "primary_goal": "weight_loss",
    "secondary_goals": ["endurance", "flexibility"],
    "resting_heart_rate": 65,
    "workout_duration_minutes": 50,
    "workouts_per_week": 4
  }'
```

**Expected Response** (201):
```json
{
  "success": true,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "alice_fitness",
  "email": "alice@example.com",
  "fitness_level": "intermediate",
  "created_at": "2024-01-15T10:00:00Z"
}
```

**Save**: `USER_ID = "550e8400-e29b-41d4-a716-446655440000"`

---

### 1.2 Retrieve User Profile
```bash
USER_ID="550e8400-e29b-41d4-a716-446655440000"

curl -X GET http://localhost:8000/fitness/users/$USER_ID/profile
```

**Expected Response** (200):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "alice_fitness",
  "email": "alice@example.com",
  "age": 28,
  "height_cm": 165,
  "weight_kg": 62,
  "fitness_level": "intermediate",
  "primary_goal": "weight_loss",
  "resting_heart_rate": 65,
  "max_heart_rate": 192,
  "workout_duration_minutes": 50,
  "workouts_per_week": 4,
  "created_at": "2024-01-15T10:00:00Z"
}
```

---

### 1.3 Update User Profile
```bash
curl -X PUT http://localhost:8000/fitness/users/$USER_ID/profile \
  -H "Content-Type: application/json" \
  -d '{
    "weight_kg": 60,
    "resting_heart_rate": 63,
    "fitness_level": "advanced",
    "primary_goal": "muscle_gain"
  }'
```

**Expected Response** (200):
```json
{
  "success": true,
  "message": "Profile updated",
  "updated_at": "2024-01-15T10:05:00Z"
}
```

---

## Phase 2: Workout Management

### 2.1 Start Workout Session
```bash
curl -X POST http://localhost:8000/fitness/users/$USER_ID/workouts \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Full Body Strength",
    "workout_type": "strength",
    "intensity": "moderate",
    "description": "Compound movements: squats, deadlifts, bench press"
  }'
```

**Expected Response** (201):
```json
{
  "success": true,
  "workout_id": "660e8400-e29b-41d4-a716-446655440001",
  "name": "Full Body Strength",
  "type": "strength",
  "intensity": "moderate",
  "started_at": "2024-01-15T06:00:00Z"
}
```

**Save**: `WORKOUT_ID = "660e8400-e29b-41d4-a716-446655440001"`

---

### 2.2 List User Workouts
```bash
curl -X GET "http://localhost:8000/fitness/users/$USER_ID/workouts?limit=5"
```

**Expected Response** (200):
```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "name": "Full Body Strength",
    "type": "strength",
    "intensity": "moderate",
    "started_at": "2024-01-15T06:00:00Z",
    "ended_at": null,
    "duration_minutes": null,
    "total_calories_burned": 0,
    "average_heart_rate": null,
    "completed": false
  }
]
```

---

## Phase 3: Exercise Tracking

### 3.1 Add Exercise to Workout
```bash
curl -X POST http://localhost:8000/fitness/workouts/$WORKOUT_ID/exercises \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Squats",
    "exercise_type": "strength",
    "muscle_groups": ["quadriceps", "glutes", "hamstrings"],
    "sets": 4,
    "reps": 8,
    "weight_kg": 80,
    "duration_seconds": 300
  }'
```

**Expected Response** (201):
```json
{
  "success": true,
  "exercise_id": "770e8400-e29b-41d4-a716-446655440002",
  "name": "Squats",
  "type": "strength",
  "started_at": "2024-01-15T06:05:00Z"
}
```

**Save**: `EXERCISE_ID = "770e8400-e29b-41d4-a716-446655440002"`

---

### 3.2 Add More Exercises
```bash
# Deadlifts
curl -X POST http://localhost:8000/fitness/workouts/$WORKOUT_ID/exercises \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Deadlifts",
    "exercise_type": "strength",
    "muscle_groups": ["back", "glutes", "hamstrings"],
    "sets": 3,
    "reps": 5,
    "weight_kg": 100,
    "duration_seconds": 240
  }'

# Bench Press
curl -X POST http://localhost:8000/fitness/workouts/$WORKOUT_ID/exercises \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bench Press",
    "exercise_type": "strength",
    "muscle_groups": ["chest", "triceps", "shoulders"],
    "sets": 4,
    "reps": 10,
    "weight_kg": 60,
    "duration_seconds": 300
  }'
```

---

## Phase 4: Biometric Tracking

### 4.1 Record Heart Rate During Warmup
```bash
curl -X POST http://localhost:8000/fitness/users/$USER_ID/biometrics \
  -H "Content-Type: application/json" \
  -d '{
    "biometric_type": "heart_rate",
    "value": 95,
    "unit": "bpm",
    "device_type": "smartwatch",
    "context": "warmup"
  }'
```

### 4.2 Record Heart Rate During Set 1 (Squats)
```bash
curl -X POST http://localhost:8000/fitness/users/$USER_ID/biometrics \
  -H "Content-Type: application/json" \
  -d '{
    "biometric_type": "heart_rate",
    "value": 135,
    "unit": "bpm",
    "device_type": "smartwatch",
    "context": "workout"
  }'
```

### 4.3 Record Multiple Biometrics
```bash
# Set 2 - Peak intensity
curl -X POST http://localhost:8000/fitness/users/$USER_ID/biometrics \
  -H "Content-Type: application/json" \
  -d '{
    "biometric_type": "heart_rate",
    "value": 150,
    "unit": "bpm",
    "device_type": "smartwatch",
    "context": "workout"
  }'

# Set 3 - Sustained
curl -X POST http://localhost:8000/fitness/users/$USER_ID/biometrics \
  -H "Content-Type: application/json" \
  -d '{
    "biometric_type": "heart_rate",
    "value": 145,
    "unit": "bpm",
    "device_type": "smartwatch",
    "context": "workout"
  }'

# Set 4 - Fatigue
curl -X POST http://localhost:8000/fitness/users/$USER_ID/biometrics \
  -H "Content-Type: application/json" \
  -d '{
    "biometric_type": "heart_rate",
    "value": 160,
    "unit": "bpm",
    "device_type": "smartwatch",
    "context": "workout"
  }'

# Recovery - Between exercises
curl -X POST http://localhost:8000/fitness/users/$USER_ID/biometrics \
  -H "Content-Type: application/json" \
  -d '{
    "biometric_type": "heart_rate",
    "value": 120,
    "unit": "bpm",
    "device_type": "smartwatch",
    "context": "recovery"
  }'
```

### 4.4 Record Other Biometrics
```bash
# Respiration rate
curl -X POST http://localhost:8000/fitness/users/$USER_ID/biometrics \
  -H "Content-Type: application/json" \
  -d '{
    "biometric_type": "respiration_rate",
    "value": 28,
    "unit": "breaths_per_minute",
    "device_type": "smartwatch",
    "context": "workout"
  }'

# Oxygen saturation
curl -X POST http://localhost:8000/fitness/users/$USER_ID/biometrics \
  -H "Content-Type: application/json" \
  -d '{
    "biometric_type": "oxygen_saturation",
    "value": 96,
    "unit": "%",
    "device_type": "smartwatch",
    "context": "workout"
  }'

# Body temperature
curl -X POST http://localhost:8000/fitness/users/$USER_ID/biometrics \
  -H "Content-Type: application/json" \
  -d '{
    "biometric_type": "body_temperature",
    "value": 37.8,
    "unit": "C",
    "device_type": "smartwatch",
    "context": "workout"
  }'
```

### 4.5 Retrieve Biometric Data
```bash
# All biometrics
curl -X GET "http://localhost:8000/fitness/users/$USER_ID/biometrics?limit=50"

# Only heart rate
curl -X GET "http://localhost:8000/fitness/users/$USER_ID/biometrics?biometric_type=heart_rate&limit=20"
```

**Expected Response**:
```json
[
  {
    "id": "880e8400-e29b-41d4-a716-446655440003",
    "type": "heart_rate",
    "value": 160,
    "unit": "bpm",
    "device_type": "smartwatch",
    "context": "workout",
    "measured_at": "2024-01-15T06:15:00Z"
  },
  {
    "id": "880e8400-e29b-41d4-a716-446655440004",
    "type": "heart_rate",
    "value": 145,
    "unit": "bpm",
    "device_type": "smartwatch",
    "context": "workout",
    "measured_at": "2024-01-15T06:16:00Z"
  }
]
```

---

## Phase 5: AI Coaching - Form Analysis

### 5.1 Analyze Push-up Form
```bash
curl -X POST http://localhost:8000/fitness/analyze/pose \
  -H "Content-Type: application/json" \
  -d '{
    "exercise_name": "push_up",
    "pose_landmarks": {
      "shoulder": {"x": 0.5, "y": 0.3, "z": 0.0},
      "elbow": {"x": 0.65, "y": 0.35, "z": 0.05},
      "wrist": {"x": 0.75, "y": 0.35, "z": 0.1},
      "hip": {"x": 0.5, "y": 0.65, "z": 0.0},
      "knee": {"x": 0.5, "y": 0.80, "z": 0.0},
      "ankle": {"x": 0.5, "y": 0.95, "z": 0.0},
      "neck": {"x": 0.5, "y": 0.2, "z": 0.0},
      "spine": {"x": 0.5, "y": 0.5, "z": 0.0}
    },
    "confidence_scores": {
      "shoulder": 0.95,
      "elbow": 0.92,
      "wrist": 0.88,
      "hip": 0.90,
      "knee": 0.91,
      "ankle": 0.89,
      "neck": 0.94,
      "spine": 0.93
    }
  }'
```

**Expected Response** (200):
```json
{
  "exercise": "push_up",
  "form_score": 85.5,
  "issues": [
    "Hips sagging - engage core",
    "Insufficient range of motion"
  ],
  "recommendations": [
    "Engage your core to prevent hip sagging",
    "Lower until chest nearly touches ground",
    "Keep elbows at ~45° from your body"
  ],
  "timestamp": "2024-01-15T06:20:00Z"
}
```

---

### 5.2 Analyze Squat Form (PERFECT FORM)
```bash
curl -X POST http://localhost:8000/fitness/analyze/pose \
  -H "Content-Type: application/json" \
  -d '{
    "exercise_name": "squat",
    "pose_landmarks": {
      "shoulder": {"x": 0.5, "y": 0.25, "z": 0.0},
      "hip": {"x": 0.5, "y": 0.45, "z": 0.0},
      "knee": {"x": 0.5, "y": 0.70, "z": 0.0},
      "ankle": {"x": 0.5, "y": 0.90, "z": 0.0},
      "left_shoulder": {"x": 0.35, "y": 0.25, "z": 0.0},
      "left_hip": {"x": 0.35, "y": 0.45, "z": 0.0},
      "right_shoulder": {"x": 0.65, "y": 0.25, "z": 0.0},
      "right_hip": {"x": 0.65, "y": 0.45, "z": 0.0}
    },
    "confidence_scores": {
      "shoulder": 0.96,
      "hip": 0.95,
      "knee": 0.94,
      "ankle": 0.92,
      "left_shoulder": 0.93,
      "left_hip": 0.92,
      "right_shoulder": 0.94,
      "right_hip": 0.93
    }
  }'
```

**Expected Response**:
```json
{
  "exercise": "squat",
  "form_score": 94.2,
  "issues": [],
  "recommendations": [
    "Maintain your excellent knee alignment",
    "Continue with proper hip drive"
  ],
  "timestamp": "2024-01-15T06:22:00Z"
}
```

---

### 5.3 Analyze Deadlift (FORM ISSUES)
```bash
curl -X POST http://localhost:8000/fitness/analyze/pose \
  -H "Content-Type: application/json" \
  -d '{
    "exercise_name": "deadlift",
    "pose_landmarks": {
      "shoulder": {"x": 0.52, "y": 0.30, "z": 0.0},
      "hip": {"x": 0.5, "y": 0.45, "z": 0.0},
      "knee": {"x": 0.5, "y": 0.70, "z": 0.0},
      "ankle": {"x": 0.5, "y": 0.90, "z": 0.0},
      "neck": {"x": 0.5, "y": 0.15, "z": 0.0},
      "spine": {"x": 0.48, "y": 0.40, "z": 0.1},
      "wrist": {"x": 0.5, "y": 0.35, "z": 0.0}
    },
    "confidence_scores": {
      "shoulder": 0.91,
      "hip": 0.90,
      "knee": 0.88,
      "ankle": 0.85,
      "neck": 0.92,
      "spine": 0.87,
      "wrist": 0.90
    }
  }'
```

**Expected Response**:
```json
{
  "exercise": "deadlift",
  "form_score": 72.3,
  "issues": [
    "Rounded back detected - keep spine neutral",
    "Bar too far from body - keep it over midfoot"
  ],
  "recommendations": [
    "Mobility work: Perform cat-cow stretches and thoracic extensions",
    "Bar too far from body - keep it over midfoot",
    "Keep bar over midfoot throughout"
  ],
  "timestamp": "2024-01-15T06:24:00Z"
}
```

---

## Phase 6: Emotion Detection

### 6.1 Calm Emotion (Low Stress Workout)
```bash
curl -X POST http://localhost:8000/fitness/analyze/emotional-state \
  -H "Content-Type: application/json" \
  -d '{
    "pupil_size": 3.5,
    "pupil_dilation_rate": 0.05,
    "blink_rate": 16,
    "eye_gaze_stability": 85,
    "heart_rate": 110
  }'
```

**Expected Response**:
```json
{
  "emotional_state": "calm",
  "confidence": 0.82,
  "timestamp": "2024-01-15T06:30:00Z"
}
```

---

### 6.2 Focused Emotion (During Heavy Lift)
```bash
curl -X POST http://localhost:8000/fitness/analyze/emotional-state \
  -H "Content-Type: application/json" \
  -d '{
    "pupil_size": 6.2,
    "pupil_dilation_rate": 0.20,
    "blink_rate": 12,
    "eye_gaze_stability": 92,
    "heart_rate": 155
  }'
```

**Expected Response**:
```json
{
  "emotional_state": "focused",
  "confidence": 0.89,
  "timestamp": "2024-01-15T06:32:00Z"
}
```

---

### 6.3 Stressed Emotion (Overexertion)
```bash
curl -X POST http://localhost:8000/fitness/analyze/emotional-state \
  -H "Content-Type: application/json" \
  -d '{
    "pupil_size": 8.1,
    "pupil_dilation_rate": 0.45,
    "blink_rate": 28,
    "eye_gaze_stability": 45,
    "heart_rate": 175
  }'
```

**Expected Response**:
```json
{
  "emotional_state": "stressed",
  "confidence": 0.85,
  "timestamp": "2024-01-15T06:34:00Z"
}
```

---

## Phase 7: Stress Detection

### 7.1 Low Stress (Warmup)
```bash
curl -X POST http://localhost:8000/fitness/analyze/stress-level \
  -H "Content-Type: application/json" \
  -d '{
    "heart_rate": 95,
    "heart_rate_variability": 85,
    "pupil_dilation_rate": 0.05,
    "respiratory_rate": 14
  }'
```

**Expected Response**:
```json
{
  "stress_level": 18,
  "interpretation": "Very Relaxed",
  "timestamp": "2024-01-15T06:36:00Z"
}
```

---

### 7.2 Moderate Stress (Main Set)
```bash
curl -X POST http://localhost:8000/fitness/analyze/stress-level \
  -H "Content-Type: application/json" \
  -d '{
    "heart_rate": 145,
    "heart_rate_variability": 45,
    "pupil_dilation_rate": 0.18,
    "respiratory_rate": 20
  }'
```

**Expected Response**:
```json
{
  "stress_level": 52,
  "interpretation": "Normal",
  "timestamp": "2024-01-15T06:38:00Z"
}
```

---

### 7.3 High Stress (Max Effort)
```bash
curl -X POST http://localhost:8000/fitness/analyze/stress-level \
  -H "Content-Type: application/json" \
  -d '{
    "heart_rate": 170,
    "heart_rate_variability": 25,
    "pupil_dilation_rate": 0.50,
    "respiratory_rate": 28
  }'
```

**Expected Response**:
```json
{
  "stress_level": 78,
  "interpretation": "Stressed",
  "timestamp": "2024-01-15T06:40:00Z"
}
```

---

## Phase 8: End Workout

### 8.1 Complete the Workout
```bash
curl -X PUT http://localhost:8000/fitness/workouts/$WORKOUT_ID/end \
  -H "Content-Type: application/json" \
  -d '{
    "mood_after": "excellent",
    "energy_after": 4,
    "pain_level": 2,
    "notes": "Great workout! Hit all targets. Felt strong throughout.",
    "ai_feedback": "Outstanding effort! Your form improved throughout the workout. Keep up the consistent breathing.",
    "completed": true
  }'
```

**Expected Response** (200):
```json
{
  "success": true,
  "message": "Workout ended",
  "workout_id": "660e8400-e29b-41d4-a716-446655440001",
  "duration_minutes": 65,
  "ended_at": "2024-01-15T07:05:00Z"
}
```

---

## Phase 9: Get Detailed Workout Info

### 9.1 Retrieve Complete Workout
```bash
curl -X GET http://localhost:8000/fitness/workouts/$WORKOUT_ID
```

**Expected Response**:
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "name": "Full Body Strength",
  "type": "strength",
  "intensity": "moderate",
  "started_at": "2024-01-15T06:00:00Z",
  "ended_at": "2024-01-15T07:05:00Z",
  "duration_minutes": 65,
  "total_calories_burned": 0,
  "average_heart_rate": 140,
  "max_heart_rate": 175,
  "min_heart_rate": 95,
  "mood_before": null,
  "mood_after": "excellent",
  "energy_before": null,
  "energy_after": 4,
  "pain_level": 2,
  "ai_feedback": "Outstanding effort!...",
  "completed": true,
  "exercises_count": 3,
  "exercises": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440002",
      "name": "Squats",
      "type": "strength",
      "sets": 4,
      "reps": 8,
      "weight_kg": 80,
      "form_score": 89.5,
      "form_issues": []
    },
    ...
  ]
}
```

---

## Phase 10: Get Statistics

### 10.1 Retrieve User Statistics
```bash
curl -X GET http://localhost:8000/fitness/users/$USER_ID/stats
```

**Expected Response** (After multiple workouts):
```json
{
  "total_workouts": 5,
  "total_workout_hours": 5.5,
  "total_calories_burned": 2125,
  "total_distance_km": 0,
  "total_steps": 0,
  "current_workout_streak": 5,
  "longest_workout_streak": 5,
  "avg_workout_duration_minutes": 66,
  "avg_heart_rate": 138,
  "avg_calories_per_workout": 425,
  "max_heart_rate_recorded": 175,
  "longest_workout_minutes": 75,
  "weekly_improvement_percent": 8.5,
  "monthly_improvement_percent": 15.2,
  "form_accuracy_trend": 4.3,
  "updated_at": "2024-01-15T10:00:00Z"
}
```

---

## Phase 11: Health Check

### 11.1 Module Health
```bash
curl -X GET http://localhost:8000/fitness/health
```

**Expected Response**:
```json
{
  "status": "healthy",
  "module": "fitness_training",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:00:00Z"
}
```

---

## Error Scenarios to Test

### User Not Found
```bash
curl -X GET http://localhost:8000/fitness/users/invalid-user-id/profile
# Expected: 404 {"detail":"User not found"}
```

### Invalid Exercise Type
```bash
curl -X POST http://localhost:8000/fitness/workouts/$WORKOUT_ID/exercises \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","exercise_type":"invalid_type","sets":1}'
# Expected: 422 Validation error
```

### Missing Required Fields
```bash
curl -X POST http://localhost:8000/fitness/users/profile \
  -H "Content-Type: application/json" \
  -d '{"username":"test"}'
# Expected: 422 Missing required field 'email'
```

---

## Performance Testing

### Load Test: Record 1000 Biometrics
```bash
for i in {1..1000}; do
  curl -X POST http://localhost:8000/fitness/users/$USER_ID/biometrics \
    -H "Content-Type: application/json" \
    -d "{\"biometric_type\":\"heart_rate\",\"value\":$((100+RANDOM%80)),\"unit\":\"bpm\"}" \
    -s > /dev/null
  
  if [ $((i % 100)) -eq 0 ]; then
    echo "Recorded $i biometrics..."
  fi
done

echo "Completed 1000 biometric recordings"
```

### Query All Biometrics
```bash
time curl -X GET "http://localhost:8000/fitness/users/$USER_ID/biometrics?limit=1000"
```

---

## Postman Collection Import

Use these sample requests to create a Postman collection:

**Variables** (Set in Postman):
```json
{
  "base_url": "http://localhost:8000",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "workout_id": "660e8400-e29b-41d4-a716-446655440001"
}
```

---

## Summary Test Checklist

- [ ] Create user profile
- [ ] Retrieve user profile
- [ ] Update user profile
- [ ] Start workout
- [ ] List workouts
- [ ] Add exercises (3+)
- [ ] Record heart rate (5+ readings)
- [ ] Record other biometrics (respiration, O2, temp)
- [ ] Retrieve all biometrics
- [ ] Analyze push-up form (good form)
- [ ] Analyze squat form (good form)
- [ ] Analyze deadlift form (poor form)
- [ ] Detect calm emotion
- [ ] Detect focused emotion
- [ ] Detect stressed emotion
- [ ] Detect low stress level
- [ ] Detect moderate stress level
- [ ] Detect high stress level
- [ ] Get workout details
- [ ] End workout
- [ ] Get user statistics
- [ ] Module health check
- [ ] Test error scenarios

---

**All tests passed** ✅ = Module ready for production!
