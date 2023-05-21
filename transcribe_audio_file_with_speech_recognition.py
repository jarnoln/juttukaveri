import argparse
import speech_recognition


def transcribe_file(speech_file):
    recognizer = speech_recognition.Recognizer()
    audio_file = speech_recognition.AudioFile(speech_file)
    with audio_file as source:
        audio = recognizer.record(source)
        result = recognizer.recognize_google(audio, language='fi-FI')
        print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file_name", help="Name of audio file to be transcribed"
    )
    args = parser.parse_args()
    transcribe_file(args.file_name)
