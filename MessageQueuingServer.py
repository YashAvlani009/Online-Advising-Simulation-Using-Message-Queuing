# Name : Yash Avlani
# UTA ID: 1001544591       NetID : yba0008
# Reference : https://docs.python.org/3/library/xmlrpc.server.html#module-xmlrpc.server
# Reference : https://github.com/thakur-nishant/Online-Advising-Simulation-using-RPC---Message-Queuing
# Reference : https://github.com/yashambre/Online-Advising-Simulation-using-RPC-Message-Queuing
# Reference : https://stackoverflow.com/questions/33359740/random-number-between-0-and-1-in-python
# Reference : https://stackoverflow.com/questions/4547274/convert-a-python-dict-to-a-string-and-back
# Reference : https://docs.python.org/3/library/tk.html
# Reference : https://stackoverflow.com/questions/27820178/how-to-add-placeholder-to-an-entry-in-tkinter

import json
import collections
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from tkinter import *
import tkinter.scrolledtext as ScrolledText
import tkinter
import tkinter as tk

import threading

import os

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler): #request handling class
    rpc_paths = ('/RPC2',)

messageQueue = {} # declare messge queue to 

def check_key(str, queue): # check if key exist in dictionary queue
    if (str in queue):
        return TRUE
    return FALSE

def append_course(student_name, course): # append a key value to the dictionary if doesn't exist in queue
    new_student = {'name': student_name, 'course': [course]}
    for i in range(len(messageQueue['course_request'])):
        if messageQueue['course_request'][i]['name'] == student_name:
            messageQueue['course_request'][i]['course'].append(course)
            break
        else:
            messageQueue['course_request'].append(new_student)

def del_key(request, option): #delete the key on specific conditions
    if option == 1:
        del messageQueue['course_request']
        return request
    if option == 2:
        del messageQueue['course_request'][0]       
        return request

    if option == 3:
        del messageQueue['course_request'][0]['course'][0]            
        return (messageQueue['course_request'][0]['name'], request)

    if option == 4:
        del messageQueue['advisor_response'][0]

    if option == 5:
        del messageQueue['advisor_response']

#classes containing all the RPC functions
class SimulationFunctions:

    def course_request(self, student_name, course): 

            new_student = {'name': student_name, 'course': [course]}
            if check_key('course_request',  messageQueue):
                if messageQueue['course_request']:
                    append_course(student_name, course)
                else:
                    messageQueue['course_request'].append(new_student)
            else:
                messageQueue['course_request'] = [new_student]
          
            print(messageQueue)
            scrollTextServer.insert(INSERT, 'In Queue : '+str(messageQueue)+'\n') # insert message in scrollerText

            return "Requested Clearence for "+course

    def advisor_queue_check(self): #check for the pending student request
                    
            scrollTextServer.insert(INSERT, 'In Queue : '+str(messageQueue)+'\n') # insert message in scrollerText

            print("Current queue:", messageQueue)
            request = 'no message found'
            if check_key('course_request', messageQueue):
                if not messageQueue['course_request']:
                   return del_key(request, 1)
                else:
                    if not messageQueue['course_request'][0]['course']:
                        return del_key(request, 2)
                    else:
                        request = messageQueue['course_request'][0]['course'][0]
                        return del_key(request, 3)
            else:
                return request

    def advisor_response(self,details,advise): #append advisor response to the dictionary key

            if check_key('advisor_response', messageQueue):
                messageQueue['advisor_response'].append([details,advise])
            else:
                messageQueue['advisor_response'] = [[details,advise]]

    def notification_process(self): #send advisor's decision in notification 

            print("Current queue:", messageQueue)

            scrollTextServer.insert(INSERT, 'In Queue : '+str(messageQueue)+'\n') # insert message in scrollerText

            request = 'no message found'
            if check_key('advisor_response', messageQueue):
                if messageQueue['advisor_response']:
                    request = messageQueue['advisor_response'][0]
                    del_key(request, 4)
                else:
                    del_key(request, 5)
            return(request)

def messageQueuingProgram():
    # Create server
    queueingServer = SimpleXMLRPCServer(("localhost", 8000), requestHandler=RequestHandler, allow_none=True)
    queueingServer.register_introspection_functions()

    print("RPC Server Start")

    print("Current queue:", messageQueue)

    queueingServer.register_instance(SimulationFunctions()) # register SimulationFunctions with server to access from other files

    # Run the server's main loop
    queueingServer.serve_forever()

def quit_Manual_Server(): #close button mannual
    print("Quit Manual")
    os._exit(0)  

def on_closing(): # default close button act
    print("Quit Default")
    quit_Manual_Server()

if __name__ == '__main__':

    
    threading.Thread(target=messageQueuingProgram).start() 
    
    master = Tk()

    lbl = Label(master, text='Message Queuing Server')
    lbl.grid(row=0)

    Button(master, text='Quit',command=quit_Manual_Server).grid(row=0, column=1, sticky=W, pady=4)

    scrollTextServer = ScrolledText.ScrolledText(master)
    scrollTextServer.grid(row=1)

    scrollTextServer.insert(INSERT, "RPC Server Start") # insert message in scrollerText

    master.mainloop()

 

