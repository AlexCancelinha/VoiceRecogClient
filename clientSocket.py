import socket
import json
import time

HOST = "localhost"
PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
test_string = {'alternative': [{'transcript': 'testing', 'confidence': 0.98762906}], 'final': True}
sock.connect((HOST, PORT))
while True:
    time.sleep(4)
    res = bytes(str(json.dumps(test_string)), 'utf-8')
    sock.sendall(res)
    sock.close()
    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print("message sent")
