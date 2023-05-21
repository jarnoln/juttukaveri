import argparse
import pyttsx3
import speech_recognition
import time


def print_tts_info(tts):
    voices = tts.getProperty('voices')
    for voice in voices:
        print(voice)
    rate = tts.getProperty('rate')
    print('Rate:')
    print(rate)


def transcribe_audio_input():
    recognizer = speech_recognition.Recognizer()
    mic = speech_recognition.Microphone()
    tts = pyttsx3.init()
    # print_tts_info(tts)
    tts.setProperty('voice', 'finnish')
    tts.setProperty('rate', 120)
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        greet = 'Sano jotain'
        print(greet)
        tts.say(greet)
        tts.runAndWait()
        time.sleep(0.5)
        while True:
            print('Kuuntelen')
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
            tts.say(result_google)
            tts.runAndWait()
            if 'heippa' in result_google.lower():
                break


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # args = parser.parse_args()
    transcribe_audio_input()
