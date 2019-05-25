# Name : Yash Avlani
# UTA ID: 1001544591       NetID : yba0008
# Reference : https://docs.python.org/3/library/xmlrpc.server.html#module-xmlrpc.server
# Reference : https://github.com/thakur-nishant/Online-Advising-Simulation-using-RPC---Message-Queuing
# Reference : https://github.com/yashambre/Online-Advising-Simulation-using-RPC-Message-Queuing
# Reference : https://stackoverflow.com/questions/33359740/random-number-between-0-and-1-in-python
# Reference : https://stackoverflow.com/questions/4547274/convert-a-python-dict-to-a-string-and-back
# Reference : https://docs.python.org/3/library/tk.html
# Reference : https://stackoverflow.com/questions/27820178/how-to-add-placeholder-to-an-entry-in-tkinter


import xmlrpc.client
from time import sleep
import random

from tkinter import *
import tkinter.scrolledtext as ScrolledText
import tkinter
import tkinter as tk

import threading

import os

scrollTextAdvisor = None # declaring scrolledText to be accessible from anywhere


#connect to the RPC server

def connect_advisor():


    clientAdvisor = xmlrpc.client.ServerProxy('http://localhost:8000')

    #check the queue continiously for available student request
    while True:
        #RPC function call to check for student request in the queue
        queueResponse = clientAdvisor.advisor_queue_check()
        print(queueResponse)
        scrollTextAdvisor.insert(INSERT, queueResponse) # insert message in scrollerText
        scrollTextAdvisor.insert(INSERT, "\n")

        if queueResponse != "no message found" and queueResponse != "":

            approval = random.choice([0, 1])
            if (approval):
                decision = 'Approved'
            else:
                decision = 'Not Approved'

            #RPC function call to append the advisor decision to the queue
            clientAdvisor.advisor_response(queueResponse,decision)
        sleep(3)


def quit_Manual_Server():
    print("Quit Manual")
    os._exit(0)  

def on_closing():
    print("Quit Default")
    quit_Manual_Server()

if __name__ == '__main__':

    
    threading.Thread(target=connect_advisor).start()

    print("TEST")
    
    master = Tk()

    lbl = Label(master, text='ADVISOR')
    lbl.grid(row=0)

    Button(master, text='Quit',command=quit_Manual_Server).grid(row=0, column=1, sticky=W, pady=4)

    scrollTextAdvisor = ScrolledText.ScrolledText(master)
    scrollTextAdvisor.grid(row=1)


    master.mainloop()




   