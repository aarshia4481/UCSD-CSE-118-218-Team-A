#Create a class audio stream that will be used to provide an endpoint for audio streaming
from time import sleep


class AudioStream:


    def getChunks(self, filepath):
        with open(filepath, 'rb') as audio_file:
            while True:
                audio_chunk = audio_file.read(1024)
                if not audio_chunk:
                    break
                yield audio_chunk

    def generate(self):

        audio_files = ["audio/test.mp3", "audio/test2.mp3", "audio/song2_parsed1.mp3"]

        for audio_file in audio_files:
            count = 0
            for chunk in self.getChunks(audio_file):


                if not chunk:
                    yield chunk
                    break
                else:

                    yield chunk
