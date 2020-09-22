import datetime 
from win32com.client import Dispatch
speak = Dispatch("SAPI.SpVoice")
import webbrowser
import os


alarmHour = int(input("What hour do you want to wake up: "))
alarmMin = int(input("What minute do you want to wake up: "))   

while True:
    if (alarmHour == datetime.datetime.now().hour and alarmMin == datetime.datetime.now().minute):
        os.startfile(r"C:\Users\Kevin\Videos\Motivation\JordanPeterson_LookAhead.mp4")
        break

print("You are awake")