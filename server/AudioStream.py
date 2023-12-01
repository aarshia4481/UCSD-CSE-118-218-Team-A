import numpy as np
#Create a class audio stream that will be used to provide an endpoint for audio streaming

class AudioStream:


    def generate(self):

        audio_file_path = 'audio/song.mp3'  # Replace with your audio file path
        song_list = ['audio/song{}.mp3'.format(i) for i in
                     range(1, 11)]  # Adjust the range to match your song filenames

        buffer_size = 1024  # Adjust buffer size as needed
        while True:
            with open(audio_file_path, 'rb') as audio_file:
                while True:
                    audio_chunk = audio_file.read(buffer_size)
                    if not audio_chunk:
                        break
                    yield audio_chunk
