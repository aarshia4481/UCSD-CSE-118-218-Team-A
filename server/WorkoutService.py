import time
from threading import Thread

from flask_pymongo import MongoClient


class WorkoutService(Thread):

    def __init__(self, session_id):
        Thread.__init__(self)
        self.session_id = session_id

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
        session_data = self.db.get_collection("workout_sessions").find_one({"session_id": self.session_id})

        participants = session_data["participants"]

        output1 = "Welcome to GroupFit! Let's get started with your workout session. Today we are " \
        + len(participants) + " participants in this session. "

        i = 0
        while True:

            if i == 20:
                break
            print("Mock workout session running...  " + self.session_id)

            # sleep for 1 second
            time.sleep(1)
            i += 1

        # check for new data in db until stopped


        print("Mock workout session finished...  " + self.session_id)

