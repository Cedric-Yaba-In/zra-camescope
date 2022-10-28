from collections import defaultdict
import socket
import sys
import time
from typing import Callable, Dict
import cv2
import pickle
import numpy as np
import struct ## new
import threading

HOST='192.168.8.101'
PORT=50000
MAX_CONNEXION=50

class ReceiveData(threading.Thread):
    """thread client object to get response from server """
    def __init__(self, drawer_function:Callable=None):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.drawer_function = drawer_function
        self.is_stopped = True
        self.is_started = False
        self.is_freezed = False
        self.start_connexion()

    def stop_connexion(self):
        self.is_stopped = True
        self.is_started = False
        self.is_freezed = False
        stop_message = "stop"
        self.my_socket.send(stop_message.encode("utf8"))
        self.my_socket.close()

    def freeze(self):
        self.is_stopped = False
        self.is_started = True
        self.is_freezed = True

    def start_connexion(self):
        try:
            self.my_socket.connect((HOST, PORT))
            self.is_stopped = False
            self.is_started = True
            self.is_freezed = False
            print("successful connected to server")
        except Exception as error:
            raise ConnectionError(f"An error occured :{error}")
        
    def get_display_data(self):
        self.is_stopped = False
        self.is_started = False
        self.is_freezed = True
        
    def set_drawer(self, drawer_function:Callable):
        self.drawer_function = drawer_function

    def run(self):
        data = bytes("", "utf8")
        payload_size = struct.calcsize("L")
        print("size", payload_size)
        while self.is_started and self.is_stopped == False:
            while len(data) < payload_size:
                v = self.my_socket.recv(4096)
                data += v
            print("len data", len(data))
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]
            print("message_size", msg_size)
            while len(data) < msg_size:
                data += self.my_socket.recv(4096)
                # print(msg_size, len(data))
            frame_data = data[:msg_size]
            data = data[msg_size:]
            ###

            frame=pickle.loads(frame_data)
            # print(frame)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            try:
                if not self.is_freezed:
                    self.drawer_function(frame)
            except Exception as error:
                print("An error occured", error)

receiver = ReceiveData()
receiver = threading.Thread(target=receiver.run)
receiver.start()