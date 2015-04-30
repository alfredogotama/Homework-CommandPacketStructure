import commandstruct as cst
import time
import socket
import pickle


IP = "127.0.0.1"
PORT = 5010

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP SEND
sock.connect((IP, PORT))

ref = cst.ROBOT_JOINT_REF()

ref.position = 1
ref.command = 1
#ref.pack()

sock.sendall(ref)
