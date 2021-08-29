# Script to spoof the date and time of a selected application
# Works by intercepting calls to GetSystemTimeAsFileTime and instead returning our spoofed time

import datetime
import frida
import os
import psutil
import tkinter as tk
from subprocess import Popen
from threading import Lock, Thread
from time import localtime, sleep, time
from tkinter import filedialog


# file dialog window
root = tk.Tk()
root.withdraw()

# user input
# convert iso date input into datetime
target = datetime.datetime.fromisoformat(input("Date String (ISO 8601): "))
# open file dialog to select application
print("Select Application")
target_path = filedialog.askopenfilename()
# split path into application and directory
target_application = target_path.split("/")[-1]
target_dir = target_path.replace(target_application,"")
# move to the directory of the application before running
os.chdir(target_dir)
# ask for debug information
debug = int(input("Debug? (1/0): "))
# run application
Popen(target_path)

# check for daylight savings time
ts = time()
dst = localtime().tm_isdst

# get the users timezone offset from utc
utc_offset = (datetime.datetime.fromtimestamp(ts) - datetime.datetime.utcfromtimestamp(ts))

# windows FILETIME epoch 
epoch = datetime.datetime(1601,1,1) + utc_offset
# convert to nanoseconds/100 (highest precision possible)
ns = ((target-epoch) / datetime.timedelta(microseconds=1)) * 10
# account for dst
ns += 10000000 * 60 * 60 * dst
# convert from float to int
ns = int(ns)
print(ns)

# set up lock
lock_session = Lock()  

def GetSystemTimeAsFileTime_hook(session):
    # listen for GetSystemTimeAsFileTime
    # on call, get the address for the FILETIME object, write our spoofed time to its location
    script = session.create_script("""

    var GetSystemTimeAsFileTime = Module.findExportByName("kernel32.dll", 'GetSystemTimeAsFileTime') // exporting the function
    Interceptor.attach(GetSystemTimeAsFileTime, { // get our pointer
        onEnter: function (args) {
            this.pointer = args[0];
        },
        onLeave: function (args) { // write our spoofed time
            send(this.pointer.writeU64(""" + str(ns) + """));

        }
    });

    """)

    # if called run log function
    script.on('message', log)
    script.load()

def log(message, data):
    # this runs whenever the application calls GetSystemTimeAsFileTime
    # print address FILETIME object
    if debug:
        print(message['payload'])

def wait_for_application():
    while True:
        # find the process
        if (target_application in (p.name() for p in psutil.process_iter())) and not lock_session.locked():
            lock_session.acquire() # Locking the thread
            print("process found")
            attach_and_hook()
            sleep(0.5)
        elif (not target_application in (p.name() for p in psutil.process_iter())) and lock_session.locked():
            lock_session.release()
            print("process is dead releasing lock")
        else:
            pass
        sleep(0.5)

def attach_and_hook():
    try:
        # attaching to the process
        print("trying to attach to process")
        session = frida.attach(target_application)
        print("attached successfully")

        # hook GetSystemTimeAsFileTime
        GetSystemTimeAsFileTime_hook(session)
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    thread = Thread(target=wait_for_application)
    thread.start()