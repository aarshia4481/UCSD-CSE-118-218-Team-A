import datetime
import uuid


class WorkoutSession(object):
    def __init__(self, session_name, creator_id):
        self.session_name = session_name
        self.creator_id = creator_id
        self.participants = [creator_id]
        self.session_id = str(uuid.uuid4())
        self.state = "created"
        self.exercise_log = []

class User:
     def __init__(self,  alexa_id, watch_id):
            self.name = "Participant"
            self.alexa_id = alexa_id
            self.watch_id = watch_id
            self.plan = WorkoutPlan()

class WorkoutPlan:
    def __init__(self, ):
        self.exercises = [{"exercise_type": "SQUATS", "reps": 10}, {"exercise_type": "CURLS", "reps": 10}, {"exercise_type": "SQUATS", "reps": 10}]
        self.date = datetime.datetime.now().date()

class HeartRateMeasurement:
    def __init__(self, timestamp, heart_rate, user_id, workout_session_name):
        self.timestamp = timestamp
        self.value = heart_rate
        self.user_id = user_id
        self.workout_session_name = workout_session_name

class ExerciseLog:
    def __init__(self, exercise_type, reps_completed, watch_id, timestamp):
        self.exercise_type = exercise_type
        self.reps_completed = reps_completed
        self.watch_id = watch_id
        self.timestamp = timestamp



