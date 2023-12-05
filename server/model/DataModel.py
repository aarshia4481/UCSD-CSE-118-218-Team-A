


# Define workout data model
import uuid


class WorkoutSession:
    def __init__(self, session_name, creator_id, participants=[]):
        self.session_name = session_name
        self.creator_id = creator_id
        self.participants = participants
        self.session_id = str(uuid.uuid4())
        self.state = "created"

# class Participant:
#     def __init__(self, name, age, gender, session_id):
#         self.name = name
#         self.age = age
#         self.gender = gender
#         self.session_id = session_id

class HeartRateMeasurement:
    def __init__(self, timestamp, heart_rate, user_id, workout_session_name):
        self.timestamp = timestamp
        self.value = heart_rate
        self.user_id = user_id
        self.workout_session_name = workout_session_name

class ExerciseLog:
    def __init__(self, exercise_type, reps_completed, participant_id, workout_session_id, timestamp):
        self.exercise_type = exercise_type
        self.reps_completed = reps_completed
        self.participant_id = participant_id
        self.workout_session_id = workout_session_id
        self.timestamp = timestamp



