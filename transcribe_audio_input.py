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
    greet = 'Sano jotain'
    print(greet)
    tts.say(greet)
    tts.runAndWait()
    while True:
        with mic as source:
            print('Default energy threshold: {}'.format(recognizer.energy_threshold))
            recognizer.adjust_for_ambient_noise(source)
            print('Adjusted Energy threshold: {}'.format(recognizer.energy_threshold))
            recognizer.energy_threshold = 1000
            print('Forced energy threshold: {}'.format(recognizer.energy_threshold))
            print('Kuuntelen')
            audio = recognizer.listen(source)
            print('Lopetin kuuntelun')
            try:
                result_google = recognizer.recognize_google(audio, language='fi-FI')
            except speech_recognition.RequestError as err:
                print('API rikki')
                print(err)
                break
            except speech_recognition.UnknownValueError as err:
                print('Sori, en saanut selvää')
                continue
            print(result_google)
            tts.say(result_google)
            tts.runAndWait()
            # time.sleep(2)
            if 'heippa' in result_google.lower():
                break


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # args = parser.parse_args()
    transcribe_audio_input()
