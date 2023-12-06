import os.path
import time
from threading import Thread

from flask_pymongo import MongoClient

from TextToSpeechService import TextToSpeechService


class WorkoutService(Thread):

    '''
    WorkoutService is a thread that runs in the background and handles the workout session.
    It is responsible for:
        - checking if there is new data from participants in the database
        - generating audio feedback for participants by calling TextToSpeechService
        - save these audio files in /audio/<session_name>
        - audio is later accessed by Alexa via url/stream_audio/<session_name>
    '''

    def __init__(self, session_id, session_name):
        Thread.__init__(self)
        self.session_id = session_id
        self.session_name = session_name
        self.tts_service = TextToSpeechService();

        #set up database
        uri = "mongodb+srv://user:cse218@groupfit.l7ynwiw.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(uri)

        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        self.db = client.get_database("groupfit")


    def run(self):

        # start mock workout session
        # get data from db

        #in workout session find participants
        session_data = self.db.get_collection("workout_sessions").find_one({"session_name": self.session_name})

        participants = session_data["participants"]

        output1 = "Welcome to GroupFit! Let's get started with your workout session. Today we are " \
        + str(len(participants)) + " participants in this session. "

        #create dictionarey at /audio/session_name
        new_folder_path = os.getcwd() + "/audio/" + self.session_name
        if not os.path.exists(new_folder_path):
            os.mkdir(os.getcwd() + "/audio/" + self.session_name)

        self.tts_service.generateAudio(self.session_name + "/output1.mp3", output1)

        i = 0
        while True:

            hr_flag = False #determine if hr was already checked


            # check lastest heart rate

            hr_datapoint = self.db.get_collection("heart_rate_measurements").find_one({"workout_session_name": self.session_name}, sort=[("timestamp", -1)])

            if hr_datapoint is not None:
                print(hr_datapoint)
                if  hr_datapoint["value"] > 80 and hr_flag == False:
                    output2 = participants[0] + " your heart rate is too high. Please take a break."
                    self.tts_service.generateAudio(self.session_name + "/output2.mp3", output2)
                    hr_flag = True


            if i == 20:
                break
            print("Mock workout session running...  " + self.session_id)

            # sleep for 1 second
            time.sleep(5)
            i += 1

        # check for new data in db until stopped


        print("Mock workout session finished...  " + self.session_id)

