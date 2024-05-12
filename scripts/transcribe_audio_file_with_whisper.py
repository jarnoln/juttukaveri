import argparse
import os
from openai import OpenAI


def transcribe_file(speech_file):
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    client = OpenAI(api_key=OPENAI_API_KEY)
    with open(speech_file, "rb") as audio_file:
        transcript = client.audio.transcribe(
            "whisper-1", file=audio_file, language="fi"
        )
        print(transcript)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", help="Name of audio file to be transcribed")
    args = parser.parse_args()
    transcribe_file(args.file_name)
