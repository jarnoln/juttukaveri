import argparse
import openai


def transcribe_file(speech_file):
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
