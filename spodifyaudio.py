from __future__ import print_function
from multiprocessing import Process, Queue
import soundcard as sc
import numpy as np
import time
import os
import sys
import scipy.signal as scipySignal
import ctypes
import psutil

mics = sc.all_microphones(include_loopback=True)
audioIn = mics[1]
RATE = 48000

CHUNK = 2048

os.system('cls')
channelsCNT = audioIn.channels
channels = range(0, audioIn.channels)

def stream(q):
    with audioIn.recorder(samplerate=RATE) as mic:
        while 1:
            data = mic.record(numframes=CHUNK)
            q.put(data)
            time.sleep(0.001)

def format_title(string):
    stringLetterCount = 0
    for letter in string:
        stringLetterCount += 1
    stringLetterCount = stringLetterCount // 2
    halfFullString = 10 - stringLetterCount
    returnString = ""
    for spaceChar in range(halfFullString):
        returnString += " "
    returnString += string
    for spaceChar in range(halfFullString):
        returnString += " "
    returnString += ""
    return returnString

def generate_percentage_bar(percentage):
    if not (0 <= percentage <= 100):
        percentage = 100
    num_chars = int(percentage / 2)
    bar = "[" + "|" * num_chars + " " * (50 - num_chars) + "]"

    return bar

def get_titles(): 
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible
    
    titles_dict = {}
    
    def foreach_window(hwnd, lParam):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            
            # Get the process ID (PID) associated with the window
            pid = ctypes.c_ulong()
            ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            
            # Get the process name from the PID
            try:
                process = psutil.Process(pid.value)
                process_name = process.name()
            except psutil.NoSuchProcess:
                process_name = "Unknown"
            
            # Use process name as the app name in the dictionary
            titles_dict[process_name] = buff.value
            
        return True
    
    EnumWindows(EnumWindowsProc(foreach_window), 0)
    return titles_dict

def update(q: Queue):
    highest_frequency = 0  # Initialize the highest frequency variable

    while True:
        while True:
            try:
                data = q.get_nowait()
            except:
                break

            for channel in channels:
                signal = np.sum(data, axis=1).real
                if channel == 0:
                    signal = scipySignal.detrend(signal)
                fft = np.abs(np.fft.fft(signal)) * 2 / (CHUNK // 2)
                fft = fft[:int(len(fft) / 2)]
                peak_index = np.argmax(fft)
                peak_frequency = peak_index * (RATE / CHUNK)

                if peak_frequency > highest_frequency:
                    highest_frequency = peak_frequency
                percentage = np.round(fft[peak_index] * 100, decimals=2)
                windowDict = get_titles()
                print(f"\r{format_title(windowDict['Spotify.exe'])} | {generate_percentage_bar(percentage)}",end='', flush=True)
    time.sleep(0.1)

if __name__ == "__main__":
    q = Queue()
    p1 = Process(target=update, args=(q,))
    p3 = Process(target=stream, args=(q,))
    p3.start()
    p1.start()
    p1.join()
    p3.join()
