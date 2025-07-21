import os 
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()

filename = os.path.dirname(__file__) + "/../utilities/downloads/But what is a neural network  Deep learning chapter 1.m4a"
print(f"Transcribing file: {filename}")

with open(filename, "rb") as file:
    transcription = client.audio.transcriptions.create(
        file = file,
        model = "whisper-large-v3-turbo",
        temperature = 0.0
    )

    print(json.dumps(transcription, indent=2, default = str))