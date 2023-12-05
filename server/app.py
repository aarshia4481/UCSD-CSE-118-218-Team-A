import json
import traceback

from flask import Flask, request, jsonify, Response, stream_with_context
from pymongo.mongo_client import MongoClient

from AudioStream import AudioStream
# # Inserting a workout session
# workout_session = WorkoutSession("2023-11-30T10:00:00", "Gym XYZ")
# mongo.db.workout_sessions.insert_one(workout_session.__dict__)
#
# # Inserting a participant
# participant = Participant("John Doe", 30, "Male", 1)  # Assuming session ID is 1
# mongo.db.participants.insert_one(participant.__dict__)
#
# # Inserting a heart rate measurement
# heart_rate_measurement = HeartRateMeasurement("2023-11-30T10:15:00", 80, 1)  # Assuming participant ID is 1
# mongo.db.heart_rate_measurements.insert_one(heart_rate_measurement.__dict__)
#
# # Inserting an exercise log
# exercise_log = ExerciseLog("Bench Press", 10, 100, "2023-11-30T10:30:00", "2023-11-30T10:35:00", 1)  # Assuming participant ID is 1
# mongo.db.exercise_logs.insert_one(exercise_log.__dict__)
from WorkoutService import WorkoutService
from model.DataModel import WorkoutSession, ExerciseLog

# Example usage:

app = Flask(__name__)

# Replace the connection string with your MongoDB URI
uri = "mongodb+srv://user:cse218@groupfit.l7ynwiw.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


db = client.get_database("groupfit")
collection = db.get_collection("workout_sessions")



@app.route('/send-workout-data', methods=['POST'])
def handle_post_request():
    if request.method == 'POST':
        try:
            # Get the JSON data sent by the client
            data = request.get_json()

            #insert new datapoint into database
            db.get_collection("exercise_logs").insert_one(ExerciseLog(data["exercise_type"], data["reps_completed"], data["participant_id"], data["workout_session_id"], data["timestamp"]).__dict__)

        except Exception:
            print("Error handling the request:")
            traceback.print_exc()
            return 'Error processing request', 400

@app.route('/create-session', methods=["POST"])
def createWorkoutSession():
    if request.method == "POST":

        #get parameters
        request_data = request.get_json()

        new_session = WorkoutSession(request_data["session_name"], request_data["creator_id"])

        #insert session into database
        db.get_collection("workout_sessions").insert_one(new_session.__dict__)

        return "", 200


@app.route('/get-sessions', methods=["GET"])
def getWorkoutSessions():
    if request.method == "GET":

        #get all sessions from database and store in data
        data = db.get_collection("workout_sessions").find({}, {"_id": 0})
        data = list(data)

        return jsonify(data)


@app.route('/join-session', methods=["POST"])
def joinWorkoutSession():
    if request.method == "POST":

        #get parameters
        join_request = request.get_json()

        with open ("data/sessions.json", "r+") as file:

            data = json.load(file)
            session_id = join_request["session_id"]

            # check if session exists in database
            session = db.get_collection("workout_sessions").find_one({"session_id": session_id}, {"_id": 0})
            print(session)

            #if session exists, add participant to session
            if session:
                session["participants"].append(join_request["user_id"])

                #update session in database
                db.get_collection("workout_sessions").update_one({"id": session_id}, {"$set": session})

                return "Joined session.", 200


            return "Session does not exist.", 400


@app.route("/finish-session", methods=["POST"])
def finsihWorkoutSession():
    if request.method == "POST":

        #get parameters
        session_id = request.get_json()["session_id"]


        # check if session exists in database
        session = db.get_collection("workout_sessions").find_one({"session_id": session_id})

        #if session exists, add participant to session
        if session:

            #update session in database
            db.get_collection("workout_sessions").update_one({"session_id": session_id}, {"$set": {"state": "finished"}})

            return "Session completed.", 200

        else:
            return "Session does not exist.", 400


@app.route("/start-session", methods=["POST"])
def startWorkoutSession():
    if request.method == "POST":

        #get parameters
        session_id = request.get_json()["session_id"]

        workout_service = WorkoutService(session_id)
        workout_service.start()

        print(session_id)


        return "Session started.", 200


@app.route('/stream_audio')
def stream_audio():


    audio_stream = AudioStream()

    return Response(audio_stream.generate(), mimetype="audio/mpeg")

@app.route('/stream_audio2')
def stream_audio2():
    audio_stream = AudioStream()



    response = Response(stream_with_context(audio_stream.generate2()), mimetype="audio/mpeg", content_type="audio/mpeg")
    ##response.headers['Content-Length'] = str(20000000)
    response.headers['Accept-Ranges'] = 'bytes'
    return response




## just for testing
@app.route('/test', methods=['GET'])
def test():

    print(client)
    print(db)
    print(collection)


    return "hello world", 200



if __name__ == '__main__':
    app.run(debug=True, port=443, ssl_context=("adhoc"))


