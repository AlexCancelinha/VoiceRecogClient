import numpy as np
import speech_recognition as sr
import torch
import whisper
r = sr.Recognizer()
audio_model = whisper.load_model("base")

while True:
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Say Something")
        audio = r.listen(source)
    # recognize speech using Sphinx
    try:
        print("Sphinx thinks you said " + r.recognize_sphinx(audio))
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    # recognize speech using whisper
    print("converting audio")
    torch_audio = torch.from_numpy(
        np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
    audio_data = torch_audio
    print("finished converting audio")
    print("Whisper thinks you said " + audio_model.transcribe(audio_data)["text"])
    '''
    try:
        print("Whisper thinks you said " + r.recognize_whisper(audio, language="english"))
    except sr.UnknownValueError:
        print("Whisper could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Whisper")
'''
