#!/usr/bin/env python3
from tkinter import *
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

class Lanchat:
    def __init__(self,root):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.BUFSIZ = 1024
        self.client_socket = socket(AF_INET, SOCK_STREAM)

    def send(self,event=None):
        self.chat_msg = self.text_box.get('1.0',END).strip()
        self.text_box.delete('1.0',END)
        if self.chat_msg == "{quit}":
            self.client_socket.close()
            self.root.destroy()
        self.client_socket.send(bytes(self.chat_msg, "utf8"))

    def on_closing(self,event=None):
        self.text_box.delete('1.0',END)
        self.text_box.insert(INSERT,"{quit}")
        self.send()

    def receive(self):
        while True:
            try:
                self.cli_msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
                self.list.insert(END,self.cli_msg)
            except OSError:
                break

    def connect(self):
        self.host_ip=self.host_input.get()
        self.host_port=int(self.port_input.get())
        self.Addr = (self.host_ip,self.host_port)
        self.client_socket.connect(self.Addr)
        self.receive_thread = Thread(target=self.receive)
        self.receive_thread.start()


    def frontend(self):
        self.MainFrame = Frame(self.root)
        self.MainFrame.pack()

        self.host = Label(self.MainFrame,text="Host",font=("Arial",15))
        self.host.grid(row=0,column=0,padx=5,pady=10)
        self.port = Label(self.MainFrame, text="Port",font=("Arial",15))
        self.port.grid(row=0,column=2,padx=5,pady=10)
        self.host_input = Entry(self.MainFrame)
        self.host_input.grid(row=0,column=1,pady=10)
        self.host_input.insert(0,'127.0.0.1')
        self.port_input = Entry(self.MainFrame)
        self.port_input.grid(row=0,column=3,pady=10)
        self.port_input.insert(0,4444)
        self.connect = Button(self.MainFrame,text="Connect",command=self.connect)
        self.connect.grid(row=0,column=4,padx=10,pady=10)

        self.ListFrame = Frame(self.root)
        self.ListFrame.pack()

        self.list = Listbox(self.ListFrame,height=25,width=80)
        self.list.grid(row=0,column=0,pady=10)
        self.lscroll = Scrollbar(self.ListFrame)
        self.lscroll.grid(row=0,column=1,padx=5,pady=10)
        self.list.configure(yscrollcommand=self.lscroll.set)
        self.lscroll.config(command=self.list.yview)
        self.list.insert(END,"Welcome To LaN ChaT!")
        self.list.insert(END,"Click connect with respective Host and Port!")

        self.MsgFrame = Frame(self.root)
        self.MsgFrame.pack()

        self.chat = Label(self.MsgFrame,text="Chat",font=("Arial",15))
        self.chat.grid(row=0,column=0,padx=10,pady=10)
        self.text_box = Text(self.MsgFrame,height=3,width=80)
        self.text_box.grid(row=0,column=1,padx=5,pady=10)
        self.tscroll = Scrollbar(self.MsgFrame)
        self.tscroll.grid(row=0,column=2,padx=5,pady=10)
        self.text_box.configure(yscrollcommand=self.tscroll.set)
        self.tscroll.config(command=self.text_box.yview)
        self.Send = Button(self.MsgFrame,text="Send",command=self.send)
        self.Send.grid(row=0,column=3,padx=5,pady=10)

root=Tk()
root.title("LaN ChaT")
gui=Lanchat(root)
gui.frontend()
root.mainloop()
