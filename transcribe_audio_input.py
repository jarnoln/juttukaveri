import argparse
import speech_recognition


def transcribe_audio_input():
    recognizer = speech_recognition.Recognizer()
    mic = speech_recognition.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            print('Sano jotain')
            audio = recognizer.listen(source)
            try:
                result_google = recognizer.recognize_google(audio, language='fi-FI')
            except speech_recognition.RequestError as err:
                print('API rikki')
                print(err)
                break
            except speech_recognition.UnknownValueError as err:
                print('Sori, en saanut selvää')
                continue
            print('Google:')
            print(result_google)
            if 'heippa' in result_google.lower():
                break


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # args = parser.parse_args()
    transcribe_audio_input()
