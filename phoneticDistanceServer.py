import socket

from g2p import make_g2p
import sys
import json

PORT = 8090
HOST = "localhost"
text_to_send = list()
transducer = make_g2p('eng', 'eng-arpabet')

phonetic_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
phonetic_server.bind((HOST, PORT))


def to_phonetic(text_to_parse):
    out = transducer(text_to_parse)
    text_to_send.append(str(out).strip())


def exec_phonetic(data_recieved):
    data_splitted = data_recieved.split(";")
    first = data_splitted[0].replace("[", "").replace("]", "").split(',')
    second = data_splitted[1]
    if data_splitted[2] == "true":
        is_list = True
    else:
        is_list = False
    if is_list:
        for possibilitie in first:
            to_phonetic(possibilitie)
    else:
        to_phonetic(second)


phonetic_server.listen()
print("Waiting for connections")
while True:
    text_to_send.clear()
    conn, addr = phonetic_server.accept()
    data = conn.recv(1024).decode(encoding="unicode_escape")
    exec_phonetic(data[2:])
    print(f"Dados recebidos: {data}")
    conn.send(str(text_to_send).encode())
    print(f"Dados enviados: {str(text_to_send)}")
    conn.close()
