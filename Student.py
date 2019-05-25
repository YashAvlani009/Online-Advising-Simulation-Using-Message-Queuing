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

from tkinter import *
import tkinter.scrolledtext as ScrolledText
import tkinter
import tkinter as tk

import threading

import os

#connect to the RPC server
clientStudent = xmlrpc.client.ServerProxy('http://localhost:8000')

class EntryWithPlaceholder(tk.Entry):  # Class to Put placeholder in Entry 

    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()


def send_message(): # function to send message for 1to1 and 1toN
    
    
    if eStudent.get() != "Student Name" and eCourse.get() != "Course Name": # check Destination is not empty
        
        scrollTextStudent.insert(INSERT, "Student Name : " + eStudent.get()  + '\n')
        scrollTextStudent.insert(INSERT, "Course Name : " + eCourse.get()  + '\n')
        scrollTextStudent.insert(INSERT, clientStudent.course_request(eStudent.get(), eCourse.get()) + '\n')

             
    else:
         
        print("Student name or Course Name Should not be empty")

def quit_Manual():
    print("Byee")
    os._exit(0)
  

def on_closing():
    quit_Manual()

if __name__ == '__main__':

    master = Tk()

    lbl = Label(master, text="STUDENT") # declaring a label
    lbl.grid(row=0)

    eCourse = EntryWithPlaceholder(master, "Course Name") # declaring message entry
    eCourse.grid(row=4, column=1)
    
    eStudent = EntryWithPlaceholder(master, "Student Name") # declaring Destination Client entry
    eStudent.grid(row=4, column=0)
    
    btn = Button(master, text='Send', command=send_message) # declaring Send button
    btn.grid(row=4, column=2)

    # declaring Quit button
    Button(master, text='Quit', command=quit_Manual).grid(row=0, column=2, sticky=W, pady=4) 

    scrollTextStudent = ScrolledText.ScrolledText(master) # scrollText for client logs
    scrollTextStudent.grid(row=2)
    
    master.protocol("WM_DELETE_WINDOW", on_closing)

    master.mainloop()