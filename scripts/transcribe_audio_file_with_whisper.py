import argparse
import openai
import os

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')


def transcribe_file(speech_file):
    openai.api_key = OPENAI_API_KEY
    with open(speech_file, "rb") as audio_file:
        transcript = openai.Audio.transcribe('whisper-1', file=audio_file, language='fi')
        print(transcript)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file_name", help="Name of audio file to be transcribed"
    )
    args = parser.parse_args()
    transcribe_file(args.file_name)
