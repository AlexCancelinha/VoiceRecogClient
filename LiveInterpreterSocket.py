import socket
import numpy as np
import speech_recognition as sr
import json
import torch
import whisper


def send_message(client_socket, message):
    if str(message) != "[]":
        print("Sending package")
        res = bytes(str(json.dumps(message)), 'utf-8')
        client_socket.send(res)
        print("sending done")
        client_socket.close()
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
    return client_socket


MODEL = "WHISPER"
TYPE_OF_WHISPER_MODEL = "small"
HOST = "localhost"
PORT = 8080
ENERGY = 300
PAUSE = 0.9
DYNAMIC_ENERGY = False


r = sr.Recognizer()
r.energy_threshold = ENERGY
r.pause_threshold = PAUSE
r.dynamic_energy_threshold = DYNAMIC_ENERGY
speech_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
speech_socket.connect((HOST, PORT))
if MODEL == "WHISPER":
    audio_model = whisper.load_model(TYPE_OF_WHISPER_MODEL)
try:
    while True:
        with sr.Microphone(sample_rate=16000) as source:
            audio = r.adjust_for_ambient_noise(source)
            print("Say Something")
            audio = r.listen(source)
        try:
            if MODEL == "GOOGLE":
                recognizer_results = r.recognize_google(audio, show_all=True)
            if MODEL == "WHISPER":
                torch_audio = torch.from_numpy(
                    np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
                audio_data = torch_audio
                recognizer_results = audio_model.transcribe(audio_data, language="english")
                recognizer_results = recognizer_results['text']
            print(recognizer_results)
            speech_socket = send_message(speech_socket, recognizer_results)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
finally:
    speech_socket.close()
