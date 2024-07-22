import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import random
import smtplib
import psutil
import cv2
import time
import pyautogui
import subprocess
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QTimer, Qt
from PyQt5.QtGui import QMovie


from dotui import Ui_dotgui

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    assname = "Dot"
    if 0 <= hour < 12:
        speak("Good Morning sir !")
    elif 12 <= hour < 18:
        speak("Good Afternoon sir !")
    else:
        speak("Good Evening sir ! ")

    # assname = ("dot")
    speak(f"I am assistant {assname}")
    # speak(assname)


class MainThread(QtCore.QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()

    def username(self):
        speak("What should I call you, sir?")
        uname = self.takecommand()
        speak("Welcome mister")
        speak(uname)

        speak("How can I help you, sir")

    def takecommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening.... ")
            r.pause_threshold = 1  # second of non-audio before a phrase is considered complete
            r.adjust_for_ambient_noise(source)          
            audio = r.listen(source)

        try:
            print("Recognizing..")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query
        except sr.RequestError:
            speak("Could not request results; check your network connection.")
            return "None"
        except sr.UnknownValueError:
            speak("I didn't catch that. Could you please repeat?")
            return "None"    
        except Exception as e:
            speak("Say that again please ...")
            print("Say that again please ...")
            return "None"

    def stopExecution(self, query):
        stop_keywords = ['stop', 'exit', 'quit', 'terminate']
        return any(keyword in query for keyword in stop_keywords)

    def shutdown(self):
        speak("Are you sure you want to shut down the system?")
        response = self.takecommand().lower()
        if 'yes' in response:
            speak("Shutting down the system")
            os.system("shutdown /s /t 1")
        else:
            speak("Shutdown cancelled")

    def restart(self):
        speak("Are you sure you want to restart the system?")
        response = self.takecommand().lower()
        if 'yes' in response:
            speak("Restarting the system")
            os.system("shutdown /r /t 1")
        else:
            speak("Restart cancelled")

    def sleep(self):
        speak("Are you sure you want to put the system to sleep?")
        response = self.takecommand().lower()
        if 'yes' in response:
            speak("Putting the system to sleep")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        else:
            speak("Sleep cancelled")

    def TaskExecution(self):
        wishMe()
        self.username()

        while True:
            query = self.takecommand().lower()

            if 'how are you' in query or 'how r u' in query:
                speak("I am fine sir, thank you")
                speak("How are you, sir")

            elif 'i am also fine' in query or 'good' in query:
                speak("It's good to know that you are fine")

            elif "what's your name" in query:
                speak("My friends call me Dot")
                print("My friends call me Dot")

            elif "change my name to" in query:
                query = query.replace("change my name to", "")
                assname = query

            elif 'change name' in query:
                speak("What would you like to call me, sir?")
                assname = self.takecommand()
                speak("Thank you sir for naming me")

            elif 'who made you' in query:
                speak("I have been created by team NHS")

            elif 'the time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Sir, the time is {strTime}")

            elif 'open youtube' in query:
                speak("Opening YouTube, sir")
                webbrowser.open("youtube.com")

            elif 'open google' in query:
                speak("Opening Google, sir")
                webbrowser.open('google.com')

            elif 'open facebook' in query:
                speak("Opening Facebook, sir")
                webbrowser.open('facebook.com')

            elif 'open instagram' in query:
                speak("Opening Instagram, sir")
                webbrowser.open('instagram.com')

            elif 'open whatsapp' in query:
                speak("Opening WhatsApp, sir")
                webbrowser.open('whatsapp.com')

            elif 'open wikipedia' in query:
                speak("Opening Wikipedia, sir")
                webbrowser.open('wikipedia.com')

            elif 'play music' in query:
                music_dir = 'C:\\Users\\ns167\\Music\\New folder'
                songs = os.listdir(music_dir)
                random.shuffle(songs) 
                print(songs)
                os.startfile(os.path.join(music_dir, songs[0]))

            elif 'open notepad' in query:
                speak("Opening Notepad, sir")
                path = "C:\\Windows\\notepad.exe"
                os.startfile(path)

            elif 'open command prompt' in query:
                speak("Opening Command Prompt")
                os.system("start cmd")

            elif 'open microsoft' in query:
                speak("Opening Microsoft Edge")
                path = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
                os.startfile(path)

            elif 'open game' in query:
                speak("Opening game, sir")
                path = 'C:\\Users\\ns167\\OneDrive\\Desktop\\Asphalt 9 Legends.lnk'
                os.startfile(path)

            elif "don't listen" in query:
                speak("For how much time do you want to stop listening to commands?")
                try:
                    a = int(self.takecommand())
                    print(f"Pausing for {a} seconds...")
                    time.sleep(a)
                    print(f"Resumed after {a} seconds.")
                except ValueError:
                    speak("Sorry, I didn't understand the time duration. Please provide a valid number.")

            elif 'open adobe' in query:
                speak("Opening Adobe, sir")
                path = 'C:\\Users\\Public\\Desktop\\Adobe Acrobat.lnk'
                os.startfile(path)

            elif 'open vs code' in query:
                speak("Opening VS Code, sir")
                path = "C:\\Users\\ns167\\OneDrive\\Desktop\\Visual Studio Code.lnk"
                os.startfile(path)

            elif 'wikipedia' in query:
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)

            elif 'shutdown' in query:
                self.shutdown()

            elif 'restart' in query:
                self.restart()

            elif 'sleep' in query:
                self.sleep()

            elif 'open camera' in query:
                speak("Opening camera")
                cap = cv2.VideoCapture(0)
                if not cap.isOpened():
                    speak("Error opening the camera. Please check if it's connected.")
                else:
                    while True:
                        ret, img = cap.read()
                        if not ret:
                            speak("Error capturing frame from the camera.")
                            break
                        cv2.imshow('webcam', img)
                        k = cv2.waitKey(50)
                        if k == 27:
                            break
                    cap.release()
                    cv2.destroyAllWindows()

            elif 'switch the window' in query:
                pyautogui.keyDown('alt')
                pyautogui.press('tab')
                pyautogui.keyUp('alt')

            elif 'close notepad' in query:  # Enable close Notepad functionality
                if self.isProcessRunning("notepad.exe"):
                    speak("Okay, sir. Closing Notepad.")
                    os.system("taskkill /f /im notepad.exe")
                else:
                    speak("Notepad is not running.")

            if self.stopExecution(query):
                speak("Stopping execution. Goodbye!")
                break


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_dotgui()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.Close)
        self.thread = MainThread()

    def startTask(self):
        self.ui.movie = QtGui.QMovie("../../../Downloads/7LP8.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("../../../Downloads/Jarvis_Loading_Screen.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("../../../Downloads/XDZT.gif")
        self.ui.label_3.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        self.thread.start()

    def showTime(self):
        current_time = QtCore.QTime.currentTime()
        current_date = QtCore.QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)

    def Close(self):
        self.thread.quit()
        self.close()

app = QtWidgets.QApplication(sys.argv)
dot = Main()
dot.show()
sys.exit(app.exec_())
