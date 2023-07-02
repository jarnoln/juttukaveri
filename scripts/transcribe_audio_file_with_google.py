import argparse
from google.cloud import speech


def transcribe_file(speech_file):
    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
            sample_rate_hertz=16000,
            language_code="fi-FI"
        )

        client = speech.SpeechClient()

        response = client.recognize(config=config, audio=audio)

        for result in response.results:
            # print(result)
            print(f"Transcript: {result.alternatives[0].transcript}")
            print(f"Confidence: {result.alternatives[0].confidence}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file_name", help="Name of audio file to be transcribed"
    )
    args = parser.parse_args()
    transcribe_file(args.file_name)
