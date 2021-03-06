#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import sys,os

#Reference From:- https://github.com/schedutron/CPAP/blob/master/Chap5/chat_serv.py
#Reference From:- https://github.com/schedutron/CPAP/blob/master/Chap5/chat_serv.py

def accept_incoming_connections():
    while True:
        try:
            client,client_address = SERVER.accept()
            print("%s:%s has connected." % client_address)
            client.send(bytes("Welcome To LaN ChaT!Type Your Name In The Chatbox And Send!","utf8"))
            addresses[client] = client_address
            Thread(target=handle_client, args=(client,)).start()
        except KeyboardInterrupt:
            sys.exit()

def handle_client(client):
    try:
        name = client.recv(BUFSIZ).decode("utf8")
        welcome = 'Welcome %s! If you ever want to quit, type {quit} and Send to exit.' % name
        client.send(bytes(welcome, "utf8"))
        msg = "%s has joined the chat!" % name
        broadcast(bytes(msg, "utf8"))
        clients[client] = name
    except KeyboardInterrupt:
        sys.exit()
    while True:
        try:
            msg = client.recv(BUFSIZ)
            if msg != bytes("{quit}", "utf8"):
                broadcast(msg, name+": ")
            else:
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del clients[client]
                broadcast(bytes("%s has left the chat." % name, "utf8"))
                break
        except KeyboardInterrupt:
            sys.exit()


def broadcast(msg, prefix=""):
    try:
        for sock in clients:
            sock.send(bytes(prefix, "utf8")+msg)
    except KeyboardInterrupt:
        sys.exit()

try:
    clients = {}
    addresses = {}

    HOST = ''
    print("Enter Port No on which you want to host the server,or just press enter to use the defult port 4444!")
    PORT = input()
    if(PORT == ""):
	    PORT = '4444'
    PORT = int(PORT)
    while(PORT > 65535):
        print("Invalid!Please Enter a value strictly less than 65536!")
        PORT = input()
        PORT = int(PORT)

    BUFSIZ = 1024
    ADDR = (HOST,PORT)

    SERVER = socket(AF_INET,SOCK_STREAM)
    SERVER.bind(ADDR)
except KeyboardInterrupt:
    sys.exit()

if __name__ == "__main__":
    try:
        SERVER.listen(5)
        print("Waiting for connection...")
        ACCEPT_THREAD = Thread(target=accept_incoming_connections)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
    except KeyboardInterrupt:
        SERVER.close()
        os._exit(1)

try:
    SERVER.close()
except KeyboardInterrupt:
    sys.exit()