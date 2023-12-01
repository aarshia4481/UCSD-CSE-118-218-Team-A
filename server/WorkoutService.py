import time
from threading import Thread


class WorkoutService(Thread):

    def __init__(self, session_id):
        Thread.__init__(self)
        self.session_id = session_id


    def run(self):

        # start mock workout session
        # get data from db

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

