from openai import OpenAI
import sys
client = OpenAI()

FILENAME = "audio/output0"
audio_file=open("{}.mp3".format(FILENAME), "rb")
transcript = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    response_format="srt"
)
with open(FILENAME + ".srt", "w") as f:
    f.write(transcript)
