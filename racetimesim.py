# Python program to illustrate a stop watch
# using Tkinter
#importing the required libraries
import tkinter as Tkinter
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import datetime as dt

raceInformation = []
counter = 1
running = False
finishedRunners = ""
finishedRacers = 0
def counter_label(timer, raceMessages, finishedEntrantsLabel):
    def count():
        if running:
            global counter
            global finishedRunners
            global raceInformation   
            global finishedRacers
                 
            nameOfFinisher = reachedFinisherTime(counter)
            if(nameOfFinisher is not None):
                finishedRunners += nameOfFinisher.name + ' finished in: ' + nameOfFinisher.time + '\n'
                finishedRacers += 1
                finishedEntrantsLabel['text'] = str(finishedRacers) + ' / ' + str(len(raceInformation)) + ' finished (' + str(len(raceInformation)) + ' Entrants)'
                raceMessages['text'] = finishedRunners

            tt = datetime.fromtimestamp(counter)
            string = tt.strftime("%H:%M:%S")
            display=string                           

            timer['text'] = display   # Or timer.config(text=display)
   
            # timer.after(arg1, arg2) delays by 
            # first argument given in milliseconds
            # and then calls the function given as second argument.
            # Generally like here we need to call the 
            # function in which it is present repeatedly.
            # Delays by 1000ms=1 seconds and call count again.
            timer.after(1000, count) 
            counter += 1
   
    # Triggering the start of the counter.
    count()     

class Entrant:
  def __init__(self, name, time, timeSeconds):
    self.name = name
    self.time = time
    self.timeSeconds = timeSeconds

def reachedFinisherTime(currentTime):
    global raceInformation

    currentTimeFloat = currentTime + 0.0

    for row in raceInformation[0:]:
        if currentTimeFloat == row.timeSeconds:
            return row

def get_total_seconds(stringHMS):
   timedeltaObj = dt.datetime.strptime(stringHMS, "%H:%M:%S") - dt.datetime(1900,1,1)
   return timedeltaObj.total_seconds()

# start function of the stopwatch
def Start(timer, raceMessages, finishedEntrantsLabel):
    global running
    global finishedRacers
    finishedRacers = 0
    running=True
    counter_label(timer, raceMessages, finishedEntrantsLabel)
    start['state'] = 'disabled'
    stop['state'] = 'normal'
    reset['state'] = 'normal'
    raceInformationButton['state'] = 'disabled'
   
# Stop function of the stopwatch
def Stop():
    global running
    start['state'] = 'normal'
    stop['state'] = 'disabled'
    reset['state'] = 'normal'
    running = False
   
# Reset function of the stopwatch
def Reset(timer, raceMessages, finishedEntrantsLabel):
    global running
    global counter
    global finishedRunners
    global finishedRacers
    global raceInformation

    finishedRacers = 0
    finishedEntrantsLabel['text'] = '0 / ' + str(len(raceInformation)) + ' finished (' + str(len(raceInformation)) + ' Entrants)'
    counter=1
    finishedRunners = ''
   
    # If rest is pressed after pressing stop.
    if running==False:      
        reset['state']= 'disabled'
        timer['text'] = '00:00:00'
        raceMessages['text'] = ''  
        raceInformationButton['state'] = 'normal'
   
    # If reset is pressed while the stopwatch is running.
    else:               
        timer['text'] = '00:00:00'
        raceMessages['text'] = ''        

def GrabRaceInformation(urlEntry, start, timer, finishedEntrantsLabel):
    global raceInformation
    raceInformation = []   

    r = requests.get(urlEntry.get())
    if r.status_code == 404:
        timer['text'] = 'Invalid URL'
        start['state'] = 'disabled'
    else:
        timer['text'] = '00:00:00'
        html = r.text
        maxTime = 0
        soup = BeautifulSoup(html, features="html.parser")
        table = soup.find('div', {"class": "race-entrants"})    
        rows = table.find_all('li')
        for row in rows[0:]:
            name = row.find_all('span', {"class": "name"})
            name = [ele.text.strip() for ele in name]
            time = row.find('time', {"class": "finish-time"})
            time = [ele.text.strip() for ele in time]
            if time[0] != "—":
                nameAndTime = Entrant(name[0], time[0], get_total_seconds(time[0]))      
                maxTime = get_total_seconds(time[0]) + 1    
                raceInformation.append(nameAndTime)
            else:
                nameAndTime = Entrant(name[0], 'DNF', maxTime)
                raceInformation.append(nameAndTime)
                maxTime += 1
            
        
        start['state'] = 'normal'
        finishedEntrantsLabel['text'] = '0 / ' + str(len(raceInformation)) + ' finished (' + str(len(raceInformation)) + ' Entrants)'        

root = Tkinter.Tk()
root.title("Racetime Simulator")
   
# Fixing the window size.
root.minsize(width=250, height=90)

timer = Tkinter.Label(root, text="00:00:00", fg="black", font="Verdana 30 bold")
raceMessages = Tkinter.Message(root, width=250)
appInfo = Tkinter.Label(root, text="Used to simulate a race \n by printing the finish times on screen \n as they would happen in a race \n \n Enter racetime URL above \n and click \"Get Race\" and then \"Start\"", fg="black", font="Verdana 10 bold")
finishedEntrantsLabel = Tkinter.Label(root, text="", fg="black", font="Verdana 10 bold")
urlEntry = Tkinter.Entry(root, width=45)
timer.pack()
raceMessages.pack()
f = Tkinter.Frame(root)
start = Tkinter.Button(f, text='Start', state='disabled', width=6, command=lambda:Start(timer, raceMessages, finishedEntrantsLabel))
stop = Tkinter.Button(f, text='Stop',width=6,state='disabled', command=Stop)
reset = Tkinter.Button(f, text='Reset',width=6, state='disabled', command=lambda:Reset(timer, raceMessages, finishedEntrantsLabel))
raceInformationButton = Tkinter.Button(f, text='Get Race',width=8, command=lambda:GrabRaceInformation(urlEntry, start, timer, finishedEntrantsLabel))
f.pack(anchor = 'center',pady=5)
finishedEntrantsLabel.pack()
start.pack(side="left")
stop.pack(side ="left")
reset.pack(side="left")
raceInformationButton.pack(side="left")
urlEntry.pack()
appInfo.pack()
root.mainloop()