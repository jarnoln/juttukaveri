import argparse
import openai
import os
import pyttsx3
import speech_recognition
# import time
import typing


OPENAI_KEY = os.environ.get('OPENAI_KEY', '')
LANGUAGE = 'fi-FI'


def print_tts_info(tts) -> None:
    voices = tts.getProperty('voices')
    for voice in voices:
        print(voice)
    rate = tts.getProperty('rate')
    print('Rate:')
    print(rate)


def create_response_text(messages: list) -> str:
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


def transcribe_audio_input(language: str, age: int) -> None:
    print('language: {}'.format(language))
    recognizer = speech_recognition.Recognizer()
    mic = speech_recognition.Microphone()
    tts = pyttsx3.init()
    # print_tts_info(tts)
    tts.setProperty('rate', 120)
    if language.startswith('fi'):
        language_code = 'fi-FI'
        tts.setProperty('voice', 'finnish')
        greet = 'Hei! Kuka sinä olet?'
        context = 'Olet ystävällinen lastenopettaja. Keskustelet {}-vuotiaan lapsen kanssa.'.format(age)
    else:
        language_code = 'en-US'
        tts.setProperty('voice', 'english')
        greet = 'Hello! What is your name?'
        context = 'You are a friendly kindergarten teacher. You are discussing with a {}-year old child.'.format(age)

    print(greet)
    tts.say(greet)
    tts.runAndWait()
    messages = [
        {"role": "system", "content": context},
        {"role": "assistant", "content": greet}
    ]

    while True:
        with mic as source:
            print('Default energy threshold: {}'.format(recognizer.energy_threshold))
            recognizer.adjust_for_ambient_noise(source)
            print('Adjusted Energy threshold: {}'.format(recognizer.energy_threshold))
            recognizer.energy_threshold = 1000
            print('Forced energy threshold: {}'.format(recognizer.energy_threshold))
            print('Listening')
            print('****************************************************************************')
            audio = recognizer.listen(source)
            print('Stopped listening')
            try:
                result_google = recognizer.recognize_google(audio, language=language_code)
            except speech_recognition.RequestError as err:
                print('API rikki')
                print(err)
                break
            except speech_recognition.UnknownValueError as err:
                print('Sorry, I did not understand that')
                continue
            print('Google speech to text:')
            print(result_google)
            messages.append({"role": "user", "content": result_google})
            print(messages)
            response = create_response_text(messages)
            messages.append({"role": "assistant", "content": response})
            tts.say(response)
            tts.runAndWait()


if __name__ == "__main__":
    if OPENAI_KEY:
        openai.api_key = OPENAI_KEY
    else:
        print('Need to set you openai key: export OPENAI_KEY={your key}')

    parser = argparse.ArgumentParser()
    parser.add_argument("--language", help="Expected input (and output) language", default='finnish')
    parser.add_argument("--age", help="User age", default=4)
    args = parser.parse_args()
    transcribe_audio_input(language=args.language, age=args.age)
