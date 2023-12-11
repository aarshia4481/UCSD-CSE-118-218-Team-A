import json
import traceback

from bson import ObjectId
from flask import Flask, request, jsonify, Response
from pymongo.mongo_client import MongoClient

from AudioStream import AudioStream
from WorkoutService import WorkoutService
from model.DataModel import WorkoutSession, ExerciseLog


''''
    This is the main file for the GroupFit backend. It handles the following:
    - serving all endpoints via Flask
    - handling requests from the alexa
    - handling requests from the watch
    '''


app = Flask(__name__)

# connect to database
uri = "mongodb+srv://user:cse218@groupfit.l7ynwiw.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)


# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


db = client.get_database("groupfit")
collection = db.get_collection("workout_sessions")


@app.route("/get-status", methods=['GET'])
def get_status():

    #get alexa_id from request
    alexa_id = request.args.get('alexa_id')

    if alexa_id is None:
        return "No alexa_id provided", 400

    #get correspoding watch_id from database
    watch_id = db.get_collection("users").find_one({"alexa_id": alexa_id})["watch_id"]

    if watch_id is None:
        return "No connected watch found", 400

    print(watch_id)

    #get workout from database, where status is created and one of the entries in participant list is the watch_id
    workout = db.get_collection("workout_sessions").find_one({"state": "created", "participants": {"$in": [watch_id]}})

    #if there is a workout, return the workout session name
    if workout is not None:
        output = "I found an exisitng workout session with the name " + workout["session_name"] + ". Would you like to start this session?"
        return jsonify(output), 200
    else:
        return "Sorry, I could not find an existing workout session. Please create a session first.", 200

@app.route("/get-plan-for-today", methods=['GET'])
def get_plan_for_today():

    #get users workout plan from database
    # atm this is just a mock saved for every user in database

    #get alexa_id from request
    alexa_id = request.args.get('alexa_id')

    if alexa_id is None:
        return "No alexa_id provided", 400

    #get user from database
    user = db.get_collection("users").find_one({"alexa_id": alexa_id})

    #if user does not exist, return error
    if user is None:
        return "No user found", 400

    #get workout plan from database
    workout_plan = db.get_collection("users").find_one({"alexa_id": alexa_id})["plan"]

    output = "Your workout plan for today is: You will do " + str(workout_plan["exercises"][0]["reps"]) + " " + workout_plan["exercises"][0]["exercise_type"] + ", " + str(workout_plan["exercises"][1]["reps"]) + " " + workout_plan["exercises"][1]["exercise_type"] + ", and " + str(workout_plan["exercises"][2]["reps"]) + " " + workout_plan["exercises"][2]["exercise_type"] + "."

    return output, 200

@app.route("/next-workout", methods=['GET'])
def get_next_workout():

    alexa_id = request.args.get('alexa_id')

    #get particpant_name from request (not required)
    participant_name = request.args.get('participant_name')

    if alexa_id is None:
        return "No alexa_id provided", 400

    #get corresponding watch_id from database
    watch_id = db.get_collection("users").find_one({"alexa_id": alexa_id})["watch_id"]

    #get workout from database, where one of the entries in participant list is the watch_id
    workout = db.get_collection("workout_sessions").find_one({"participants": {"$in": [watch_id]}})

    #get logs from this workout for watch_id
    logs = workout["exercise_log"]

    if logs == []:
        return "Sorry, there are no records for this participant in your session", 200

    #get all logs where datatype and watch_id is equal to watch_id or if participant is specified get their logs

    if participant_name is None:
        logs_for_watch_id = [log for log in logs if log['watch_id'] == watch_id]
    else:
        #get watch_id for participant
        #parse name to lowercase
        participant_name = participant_name.lower()

        #get in database
        watch_id = db.get_collection("users").find_one({"name": participant_name})["watch_id"]
        print(watch_id)

        #get last log with matching watch_id
        logs_for_watch_id = [log for log in logs if log['watch_id'] == watch_id]

    exercise_logs = [log for log in logs_for_watch_id if log['datatype'] != "HEARTRATE"]

    latest_log = max(exercise_logs, key=lambda x: x['timestamp'])

    if latest_log["datatype"] == "SQUAT":
        output = "Your next exercise is Curls. Please start the exercise when you are ready."
    else:
        output = "Your next exercise is Squats. Please start the exercise when you are ready."
        

    return output, 200

@app.route("/get-workout-live-metrics", methods=['GET'])
def get_workout_live_metrics():

    #get alexa_id from request
    alexa_id = request.args.get('alexa_id')

    #get particpant_name from request
    participant_name = request.args.get('participant_name')



    if alexa_id is None:
        return "No alexa_id provided", 400

    # get corresponding watch_id from database
    watch_id = db.get_collection("users").find_one({"alexa_id": alexa_id})["watch_id"]

    # get workout from database, where status is ongoing and one of the entries in participant list is the watch_id
    workout = db.get_collection("workout_sessions").find_one(
        {"participants": {"$in": [watch_id]}})

    print(workout)

    if participant_name is None:
        # endpoint servers live metrics for participant that is currently talking to alexa


        #get logs from this workout
        logs = workout["exercise_log"]

        if logs == []:
            return "Sorry, I could not find any logs for this participant in your session", 200

        #get last log with matching watch_id
        logs_for_watch_id = [log for log in logs if log['watch_id'] == watch_id]

        if not logs_for_watch_id:
            return None  # No logs found for the given watch_id

        heartrate_logs = [log for log in logs_for_watch_id if log['datatype'] == "HEARTRATE"]
        exercise_logs = [log for log in logs_for_watch_id if log['datatype'] != "HEARTRATE"]

        if not heartrate_logs == []:
            heartrate_average = sum([log["value"] for log in heartrate_logs]) / len(heartrate_logs)
        else:
            heartrate_average = 0

        latest_log = max(exercise_logs, key=lambda x: x['timestamp'])

        output = "You have completed " + str(latest_log["value"]) + " " + latest_log["datatype"] + "." + "The avg heart rate for this exercise was " + str(heartrate_average) + " beats per minute."

        return output, 200

    else:
        # endpoint serves live metrics for a specific participant in the session

        #get logs from this workout
        logs = workout["exercise_log"]

        if logs == []:
            return "Sorry, I could not find any logs for this participant in your session", 200

        #get watch_id for participant
        #parse name to lowercase
        participant_name = participant_name.lower()

        print(participant_name)
        watch_id = db.get_collection("users").find_one({"name": participant_name})["watch_id"]

        #get last log with matching watch_id
        logs_for_watch_id = [log for log in logs if log['watch_id'] == watch_id]

        if not logs_for_watch_id:
            return "Sorry, I could not find any logs for this participant in your session", 200

        heartrate_logs = [log for log in logs_for_watch_id if log['datatype'] == "HEARTRATE"]
        exercise_logs = [log for log in logs_for_watch_id if log['datatype'] != "HEARTRATE"]

        if not heartrate_logs == []:
            heartrate_average = sum([log["value"] for log in heartrate_logs]) / len(heartrate_logs)
        else:
            heartrate_average = 0

        latest_log = max(exercise_logs, key=lambda x: x['timestamp'])

        output = participant_name + " has completed " + str(latest_log["value"]) + " " + latest_log["datatype"] + "." + "The avg heart rate for this exercise was " + str(heartrate_average) + " beats per minute."
        return output, 200


@app.route("/get-workout-summary", methods=['GET'])
def get_workout_summary():

    #get alexa_id from request
    alexa_id = request.args.get('alexa_id')

    #get particpant_name from request (not required)
    participant_name = request.args.get('participant_name')

    if alexa_id is None:
        return "No alexa_id provided", 400

    #get corresponding watch_id from database
    watch_id = db.get_collection("users").find_one({"alexa_id": alexa_id})["watch_id"]

    #get workout from database, where one of the entries in participant list is the watch_id
    workout = db.get_collection("workout_sessions").find_one({"participants": {"$in": [watch_id]}})

    #get logs from this workout for watch_id
    logs = workout["exercise_log"]

    if logs == []:
        return "Sorry, there are no records for this participant in your session", 200

    #get all logs where datatype and watch_id is equal to watch_id or if participant is specified get their logs

    if participant_name is None:
        logs_for_watch_id = [log for log in logs if log['watch_id'] == watch_id]
    else:
        #get watch_id for participant
        #parse name to lowercase
        participant_name = participant_name.lower()

        #get in database
        watch_id = db.get_collection("users").find_one({"name": participant_name})["watch_id"]
        print(watch_id)

        #get last log with matching watch_id
        logs_for_watch_id = [log for log in logs if log['watch_id'] == watch_id]



    if not logs_for_watch_id:
        return "Sorry, there are no records for this participant in your session", 200

    #get all logs where datatype is equal to heartrate
    heartrate_logs = [log for log in logs_for_watch_id if log['datatype'] == "HEARTRATE"]
    print(heartrate_logs)

    #get all logs where datatype is unequal to heartrate
    exercise_logs = [log for log in logs_for_watch_id if log['datatype'] != "HEARTRATE"]
    print(exercise_logs)
    print(watch_id)

    #determine start and end time of workout parse timestamp to milliseconds
    start = int(exercise_logs[0]["timestamp"])
    end = int(exercise_logs[-1]["timestamp"])

    #calculate duration in minutes and seconds (timestamp in milliseconds)
    duration = (end - start) / 1000

    #form a string to min and seconds
    duration = str(int(duration/60)) + " minutes and " + str(int(duration%60)) + " seconds"

    #calculate heartrate average
    if not heartrate_logs == []:
        heartrate_average = sum([log["value"] for log in heartrate_logs]) / len(heartrate_logs)
    else:
        heartrate_average = 0

    if participant_name is None:
        output = "You have completed " + str(len(exercise_logs)) + " repetitions in " + duration + " seconds. Your average heart rate was " + str(heartrate_average) + " beats per minute."
    else:
        output = participant_name + " has completed " + str(len(exercise_logs)) + " repetitions in " + duration + " seconds." + participant_name + "average heart rate was " + str(heartrate_average) + " beats per minute. "

    return output, 200

@app.route('/send-workout-data', methods=['POST'])
def handle_post_request():
    if request.method == 'POST':
        try:
            # Get the JSON data sent by the client
            data = request.get_json()


            #get workout session name from request

            workout_session_name = data["workout_session_name"]

            #find workout session in database
            workout_session = db.get_collection("workout_sessions").find_one({"session_name": workout_session_name})

            #append data to exercise log
            workout_session["exercise_log"].append(data)

            #save workout session in database
            db.get_collection("workout_sessions").replace_one({"session_name": workout_session_name}, workout_session)

            return 'Data saved.', 200

        except Exception as e:
            print("Error handling the request:")
            print(e)
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

        session_dict = new_session.__dict__
        for key, value in session_dict.items():
            if isinstance(value, ObjectId):
                session_dict[key] = str(value)  # Convert ObjectId to string


        return json.dumps(session_dict), 200


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

        # check if session exists in database
        session = db.get_collection("workout_sessions").find_one({"session_name": join_request["session_name"]})

        #if session exists, add participant to session
        if session:

                #update session in database
                db.get_collection("workout_sessions").update_one({"session_name": join_request["session_name"]}, {"$push": {"participants": join_request["user_id"]}})

                #retrieve new session data
                updated_session = db.get_collection("workout_sessions").find_one({"session_name": join_request["session_name"]})


                for key, value in updated_session.items():
                    if isinstance(value, ObjectId):
                        updated_session[key] = str(value)  # Convert ObjectId to string

                return json.dumps(updated_session), 200


        else:
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

        session_name = request.get_json()["session_name"]
        session_id = ""

        workout_service = WorkoutService(session_id, session_name)
        workout_service.start()

        print(session_id)


        return "Session started.", 200

@app.route("/get-participants", methods=["GET"])
def getParticipants():
    if request.method == "GET":

        #get parameters
        session_name = request.args.get("session_name")

        if session_name == None:
            return "No session name provided.", 400

        # check if session exists in database
        participants = db.get_collection("workout_sessions").find_one({"session_name": session_name})["participants"]



        return jsonify({"participants": participants}), 200


@app.route('/stream_audio/')
def stream_audio():

    if request.method == 'GET':
        session_id = request.args.get('session_name')

    if session_id == None:
        return "No session name provided.", 400


    audio_stream = AudioStream(session_id)

    return Response(audio_stream.generate(), mimetype="audio/mpeg")



## just for testing
@app.route('/test', methods=['GET'])
def test():

    print(client)
    print(db)
    print(collection)


    return "hello world", 200


@app.route('/', methods=['GET'])
def index():
    try:
        # Read the content of the README.md file
        with open('README.md', 'r') as file:
            readme_content = file.read()

        # Return the README content as the response
        return readme_content, 200, {'Content-Type': 'text/plain'}
    except FileNotFoundError:
        return "README.md not found", 404



if __name__ == '__main__':
    app.run(debug=True, ssl_context=("adhoc"))

    #port 443


