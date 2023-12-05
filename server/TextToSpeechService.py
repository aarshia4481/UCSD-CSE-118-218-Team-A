import requests

from dotenv import load_dotenv
import os



class TextToSpeechService:
    # Load variables from the .env file
    load_dotenv()

    def __init__(self):
        self.subscription_key = os.getenv("API_KEY_TTS_AWS")
        self.tts_endpoint = 'https://westus.api.cognitive.microsoft.com/'



    def generateAudio(self, filename, text):


        url = f"https://westus.tts.speech.microsoft.com/cognitiveservices/v1"
        headers = {
            "Ocp-Apim-Subscription-Key": self.subscription_key,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3",
            "User-Agent": "curl"
        }
        data = """
        <speak version='1.0' xml:lang='en-US'>
            <voice xml:lang='en-US' xml:gender='Female' name='en-US-JennyNeural'>{}</voice>
        </speak>
        """

        data = data.format(text)

        response = requests.post(url, headers=headers, data=data, stream=True)
        if response.status_code == 200:
            with open('audio/' + filename, 'wb') as audio_file:
                for chunk in response.iter_content(chunk_size=1024):
                    audio_file.write(chunk)
            print("MP3 file saved as  " + filename + ".")
        else:
            print("Failed to generate MP3:", response.status_code, response.text)


if __name__ == "__main__":
        audio_service = TextToSpeechService()
        audio_service.generateAudio("test.mp3")
