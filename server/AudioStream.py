import os
from time import sleep


class AudioStream:


    def __init__(self, session_name):
        self.session_name = session_name

    def get_files_in_folder(self, folder_path):
        files_list = []
        for file in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, file)):
                files_list.append(file)
        return files_list




    def generate(self):
        # build audio file path from session id
        audio_dict = "audio/" + self.session_name

        # get all audio files from audio_dict
        audio_files = self.get_files_in_folder(audio_dict)
        audio_files_count = len(audio_files)

        print(audio_dict)
        print(audio_files_count)

        # Track the last played audio file index
        play_index = 0

        while True:

            while play_index < audio_files_count:
                print("Play now: " + str(play_index))


                audio_file_path = audio_files[play_index]


                with open(audio_dict + "/" + audio_file_path, 'rb') as audio_file:
                        while True:
                            audio_chunk = audio_file.read(1024)
                            if not audio_chunk:
                                play_index += 1
                                sleep(7)
                                break

                            yield audio_chunk


            # If no new audio files, play the fallback audio in a loop
            while play_index >= audio_files_count:
                print("fallback")
                fallback_audio_file = 'audio/song2_parsed1.mp3'  # Replace with your fallback audio

                with open(fallback_audio_file, 'rb') as fallback_audio:
                    while True:
                        audio_chunk = fallback_audio.read(1024)
                        if not audio_chunk:
                            sleep(7)
                            break

                        yield audio_chunk

                # Check for new audio files after playing the fallback
                audio_files = self.get_files_in_folder(audio_dict)
                audio_files_count = len(audio_files)

    def check_for_new_files(self, audio_dict, audio_files, current_count):
        # Logic to check for new audio files or changes in the folder
        updated_files = self.get_files_in_folder(audio_dict)
        if updated_files != audio_files:
            audio_files.clear()
            audio_files.extend(updated_files)
