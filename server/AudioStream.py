import os
from time import sleep


class AudioStream:


    def __init__(self, session_id):
        self.session_id = session_id

    def get_files_in_folder(self, folder_path):
        files_list = []
        for file in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, file)):
                files_list.append(file)
        return files_list


    def getChunks(self, filepath):
        with open(filepath, 'rb') as audio_file:
            while True:
                audio_chunk = audio_file.read(1024)
                if not audio_chunk:
                    break
                yield audio_chunk


    def generate(self):
        # build audio file path from session id
        audio_dict = "audio/" + self.session_id

        # get all audio files from audio_dict
        audio_files = self.get_files_in_folder(audio_dict)
        audio_files_count = len(audio_files)

        print(audio_files_count)

        # Track the last played audio file index
        last_played_index = 0

        while True:
            # Loop through audio files starting from the last played index
            while last_played_index < audio_files_count:
                print(last_played_index)
                print("playing")
                sleep(5)
                audio_file = audio_files[last_played_index+1]
                for chunk in self.getChunks(os.path.join(audio_dict, audio_file)):
                    if not chunk:
                        last_played_index += last_played_index  # Update last played index
                        break
                    yield chunk


            # If no new audio files, play the fallback audio in a loop
            while last_played_index >= audio_files_count:
                print("fallback")
                fallback_audio_file = 'audio/song2_parsed1.mp3'  # Replace with your fallback audio
                for chunk in self.getChunks(os.path.join(audio_dict, fallback_audio_file)):
                    if not chunk:
                        break
                    yield chunk

                # Check for new audio files after playing the fallback
                self.check_for_new_files(audio_dict, audio_files, audio_files_count)
                audio_files_count = len(audio_files)

    def check_for_new_files(self, audio_dict, audio_files, current_count):
        # Logic to check for new audio files or changes in the folder
        updated_files = self.get_files_in_folder(audio_dict)
        if updated_files != audio_files:
            audio_files.clear()
            audio_files.extend(updated_files)
