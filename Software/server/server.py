import base64
from io import BytesIO
import socket
import time
from typing import Callable, Dict
import cv2
import pickle
import numpy as np
import struct ## new
import threading
import random
import json

HOST='192.168.8.101'
PORT=50000
MAX_CONNEXION=50

class ClientInformation:
    id:int = None
    connexion:socket.socket = None
    adress:str = None
    port:int = None


class ClientThread(threading.Thread):
    def __init__(self, connexion:socket.socket, id:int, disconnect_function:Callable):
        threading.Thread.__init__(self)
        self.connexion = connexion
        self.id = id
        self.disconnect_function = disconnect_function
    
    def run(self):
        while True:
            try:
                message_client = self.connexion.recv(1024).decode("Utf8")
                if message_client.lower().strip() in ["stop", "close"]:
                    break
            except Exception as error:
                break
        self.disconnect_function(self.id)


class Server:
    def __init__(self):
        self.connexions = {}
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.count_connexion = 0
        self.is_listen_connection = False
        self.clients:Dict[int, ClientInformation] = {}

        try:
            self.my_socket.bind((HOST, PORT))
            print("server is started")
        except Exception as error:
            raise ConnectionError(f"An error occured :{error}")
    
    def _disconnect_function(self, id:int):
        self.clients[id].connexion.close()
        self.clients.pop(id)

    def send_data_to_clients(self):
        cap=cv2.VideoCapture(0)
        while True:
            try:
                ret,frame=cap.read()
                data = pickle.dumps(frame)
                for id in self.clients:
                    self.clients[id].connexion.sendall(struct.pack("L", len(data))+data) 
                time.sleep(10*(1/1000)) #wait 10ms
            except Exception as error:
                print(error)

    def start_listen_connexion(self):
        while True:
            if self.is_listen_connection == False:
                if self.count_connexion < MAX_CONNEXION:
                    self.is_listen_connection = True
                    thread = threading.Thread(target=self._listen_connexion)
                    thread.daemon = True
                    thread.start()
            time.sleep(.1)
        
    def _generate_id(self):
        return random.randint(1, 100000000)

    def _listen_connexion(self):
        print("start listen")
        self.my_socket.listen(MAX_CONNEXION)
        while self.count_connexion < MAX_CONNEXION:
            try:
                connexion, adress = self.my_socket.accept()
                client = ClientInformation()
                client.id = self._generate_id()
                client.connexion = connexion
                client.adress = adress[0]
                client.port = adress[1]
                self.clients[client.id] = client
                client_thread = ClientThread(connexion=connexion, id=client.id, disconnect_function=self._disconnect_function)
                client_thread.daemon = True
                client_thread.start()

                print(f"new client with ip : {client.adress} and port: {client.port} is connected")

                self.count_connexion += 1
            except Exception as error:
                pass
        self.is_listen_connection = False
    
    def start(self):
        start_listen = threading.Thread(target=self.start_listen_connexion)
        start_listen.daemon = True
        start_listen.start()

        send_data = threading.Thread(target=self.send_data_to_clients)
        send_data.daemon = True
        send_data.start()

        while True:
            pass


server = Server()
server.start()