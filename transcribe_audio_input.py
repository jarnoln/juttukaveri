import argparse
import openai
import os
import pyttsx3
import speech_recognition
import time


OPENAI_KEY = os.environ.get('OPENAI_KEY', '')


def print_tts_info(tts):
    voices = tts.getProperty('voices')
    for voice in voices:
        print(voice)
    rate = tts.getProperty('rate')
    print('Rate:')
    print(rate)


def create_response_text(messages):
    print('Sending messages:')
    print(messages)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    print(response)
    response_text = response.choices[0]['message']['content']
    print(response_text)
    return response_text


def transcribe_audio_input():
    recognizer = speech_recognition.Recognizer()
    mic = speech_recognition.Microphone()
    tts = pyttsx3.init()
    # print_tts_info(tts)
    tts.setProperty('voice', 'finnish')
    tts.setProperty('rate', 120)
    greet = 'Hei! Kuka sinä olet?'
    print(greet)
    tts.say(greet)
    tts.runAndWait()
    messages = [
        {"role": "system", "content": "Olet ystävällinen lastenopettaja. Keskustelet 4-vuotiaan lapsen kanssa."},
        {"role": "assistant", "content": greet}
    ]
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
            if result_google.strip():
                if 'heippa' or 'riittää' in result_google.lower():
                    break
                messages.append({"role": "user", "content": result_google})
                response = create_response_text(messages)
                messages.append({"role": "assistant", "content": response})
                tts.say(response)
                tts.runAndWait()
            # time.sleep(2)


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # args = parser.parse_args()
    if OPENAI_KEY:
        openai.api_key = OPENAI_KEY
    else:
        print('Need to set you openai key: export OPENAI_KEY={your key}')
    transcribe_audio_input()
