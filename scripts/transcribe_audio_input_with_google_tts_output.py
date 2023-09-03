import speech_recognition
import time
from google.cloud import texttospeech
import pyttsx3
from playsound import playsound


def say(client, text):
    voice = texttospeech.VoiceSelectionParams(language_code='fi-FI')
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)
    synthesis_input = texttospeech.SynthesisInput(text=text)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    # print(response)
    with open("output.wav", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.wav"')
    playsound('output.wav')


def transcribe_audio_input():
    recognizer = speech_recognition.Recognizer()
    mic = speech_recognition.Microphone()
    tts_client = texttospeech.TextToSpeechClient()
    say(tts_client, 'Heippa vaan')
    tts = pyttsx3.init()
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
                print(err)
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
