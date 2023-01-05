import speech_recognition as sr
import json
import pickle

r = sr.Recognizer()
while True:
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Say Something")
        audio = r.listen(source)
    try:
        recognizer_results = r.recognize_google(audio, show_all=True)
        print(recognizer_results)
        json_to_send = json.dumps(recognizer_results)
        print(json_to_send)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
