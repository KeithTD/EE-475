#!/usr/bin/python3

import tkinter as tk
from tkinter import *
import time, serial
from PIL import ImageTk, Image
import random

#BOO
random.seed()
ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)
ser.close()
ser.open()

#global var for clock
time1 = ''
#global var for dots
count = -1
#global var for RFID type/days to be sent out
addType=''
addDays=list('mtwrfsn')
scanDay=''
user=''

#def clicked(str1):
#    ser.write(str.encode(str1))

def oneSelect(btn, btn1, btn2, btn3, day):
    global addType
    if btn['bg'] == 'red':
        btn['bg'] = 'blue'
        btn['activebackground'] = 'blue'
        addType = day
        if btn1['bg'] == 'blue':
            btn1['bg'] = 'red'
            btn1['activebackground'] = 'red'
        if btn2['bg'] == 'blue':
            btn2['bg'] = 'red'
            btn2['activebackground'] = 'red'
        if btn3['bg'] == 'blue':
            btn3['bg'] = 'red'
            btn3['activebackground'] = 'red'
    else:
        btn['bg'] = 'red'
        btn['activebackground'] = 'red'
        addType=''
        
def oneUserSelect(master, btn, btn1, btn2, btn3, name):
    global user
    if btn['bg'] == 'red':
        btn['bg'] = 'blue'
        btn['activebackground'] = 'blue'
        user = name
        if btn1['bg'] == 'blue':
            btn1['bg'] = 'red'
            btn1['activebackground'] = 'red'
        if btn2['bg'] == 'blue':
            btn2['bg'] = 'red'
            btn2['activebackground'] = 'red'
        if btn3['bg'] == 'blue':
            btn3['bg'] = 'red'
            btn3['activebackground'] = 'red'
    else:
        btn['bg'] = 'red'
        btn['activebackground'] = 'red'
        user=''
    master.switch_frame(PageOne)

def oneDaySelect(btn, btn1, btn2, btn3, btn4, btn5, btn6, day):
    global scanDay
    if btn['bg'] == 'red':
        btn['bg'] = 'blue'
        btn['activebackground'] = 'blue'
        scanDay = day
        if btn1['bg'] == 'blue':
            btn1['bg'] = 'red'
            btn1['activebackground'] = 'red'
        if btn2['bg'] == 'blue':
            btn2['bg'] = 'red'
            btn2['activebackground'] = 'red'
        if btn3['bg'] == 'blue':
            btn3['bg'] = 'red'
            btn3['activebackground'] = 'red'
        if btn4['bg'] == 'blue':
            btn4['bg'] = 'red'
            btn4['activebackground'] = 'red'
        if btn5['bg'] == 'blue':
            btn5['bg'] = 'red'
            btn5['activebackground'] = 'red'
        if btn6['bg'] == 'blue':
            btn6['bg'] = 'red'
            btn6['activebackground'] = 'red'
    else:
        btn['bg'] = 'red'
        btn['activebackground'] = 'red'
        scanDay=''

def allSelect(btn, num):
    if btn['bg'] == 'red':
        btn['bg'] = 'blue'
        btn['activebackground'] = 'blue'
        addDays[num] = addDays[num].upper()
    else:
        btn['bg'] = 'red'
        btn['activebackground'] = 'red'
        addDays[num] = addDays[num].lower()

def deleteRFID(master):
    master.switch_frame(PageNine)
    ser.write(str.encode('3dd'))

def addRFID(master):
    master.switch_frame(PageNine)
    entry = '2'
    for i in range(7):
        if addDays[i].isupper():
            entry += addDays[i]
    entry += addType
    entry += 'd'
    
    ser.write(str.encode(entry))

def modRFID(master):
    master.switch_frame(PageNine)
    entry = '3m'
    for i in range(7):
        if addDays[i].isupper():
            entry += addDays[i]
    entry += 'd'
    
    ser.write(str.encode(entry))

def scanRFID(master):
    master.switch_frame(PageNine)
    entry = '1' + scanDay
    ser.write(str.encode(entry))

def listRFID(master):
    master.switch_frame(PageNine)
    entry = '4' + user
    ser.write(str.encode(entry))
    
#Initialize GUI
class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.attributes("-fullscreen", False)
        self.configure(background='black')
        self.bind("<Escape>", lambda event: self.attributes("-fullscreen", False))
        self.bind("<F11>", lambda event: self.attributes("-fullscreen", True))
        self.bind("<F9>", lambda event: self.destroy())
        self.geometry('800x480')
        self._frame = None
        self.switch_frame(StartPage)
        
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill=BOTH, expand=True)
        

#Welcome Screen/Clock
class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='black')
        
        file = str(random.randrange(1, 5))
        file = "/home/pi/run/" + file + ".jpg"
        self.background = ImageTk.PhotoImage(Image.open(file))
        canvas = tk.Canvas(self, width=800, height=480, bg='blue')
        canvas.pack(expand = tk.YES, fill = tk.BOTH)
        canvas.create_image(0, 0, image = self.background, anchor = tk.NW)

        btn = Button(self, text="Menu", font=('Helvetica', 55, "bold"), activebackground='red',
                     bg='red', command=lambda:master.switch_frame(PageNineteen))
        btn.place(x=400, y=480, anchor="s")

        tk.Button(self, text="Debug", font=('Helvetica', 24, "bold"), activebackground='blue',
                     bg='blue', command=lambda:master.switch_frame(pageList[11])).place(x=800, y=480, anchor="se")
        
        global clock
        clock = canvas.create_text(400, 0, text=time1, anchor="n", fill='white', font=('Helvetica', 100,"bold"))

        while ser.inWaiting():
            ser.read()

        def task():
            if ser.inWaiting():
                entry = ser.read()
                entry = entry.decode('utf-8')
                if entry=='b':
                    master.switch_frame(PageNine)
                    return
            self.after(500, task)
        def tick():
            global time1
            global clock
            time2 = time.strftime('%H:%M')
            if time2 != time1:
                time1 = time2
                canvas.delete(clock)
                clock = canvas.create_text(400, 0, text=time2, anchor="n", fill='white', font=('Helvetica', 100,"bold"))
            self.after(200, tick)
        tick()
        task()
        

#Main Menu
class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='black')

        greeting = "Hello, "
        if user == 'g':
            greeting+="Gavin!"
        if user == 'j':
            greeting+="John!"
        if user == 'k':
            greeting+="Keith!"
        if user == 'r':
            greeting+="Rei!"
            
        tk.Label(self, text=greeting, fg='red', bg='black', font=('Helvetica', 48,
                                                                "bold")).place(x=400, y=0, anchor="n")
        tk.Button(self, text="   Add a new RFID   ", font=('Helvetica', 36, "bold"), activebackground='red',
                     bg='red', command=lambda:master.switch_frame(PageTwo)).place(x=400, y=155, anchor="s")
        tk.Button(self, text="Modify/Delete an RFID", font=('Helvetica', 36, "bold"), activebackground='red',
                     bg='red', command=lambda:master.switch_frame(PageThree)).place(x=400, y=255, anchor="s")
        tk.Button(self, text="    Manual Scan    ", font=('Helvetica', 36, "bold"), activebackground='red',
                     bg='red', command=lambda:master.switch_frame(PageFour)).place(x=400, y=355, anchor="s")
        tk.Button(self, text="      RFID List      ", font=('Helvetica', 36, "bold"), activebackground='red',
                     bg='red', command=lambda:listRFID(master)).place(x=400, y=455, anchor="s")
        tk.Button(self, text="Back", font=('Helvetica', 36, "bold"), activebackground='blue',
                     bg='blue', command=lambda:master.switch_frame(PageNineteen)).place(x=0, y=480, anchor="sw")
        self.after(60000, master.switch_frame, StartPage)
        

#Add RFID Menu
class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='black')

        global addDays, addType
        addDays=list('mtwrfsn')
        addType=''
        
        tk.Label(self, text="Add RFID?", fg='red', bg='black', font=('Helvetica', 36,
                                                                 "bold", "underline")).place(x=400, y=15, anchor="n")
        btn1 = tk.Button(self, text="Textbook", font=('Helvetica', 30, "bold"), activebackground='red',
                     bg='red', command=lambda:oneSelect(btn1, btn2, btn3, btn4, 't'))
        btn1.place(x=125, y=160, anchor="s")
        btn2 = tk.Button(self, text="Notebook", font=('Helvetica', 30, "bold"), activebackground='red',
                     bg='red', command=lambda:oneSelect(btn2, btn1, btn3, btn4, 'n'))
        btn2.place(x=335, y=160, anchor="s")
        btn3 = tk.Button(self, text=" Laptop ", font=('Helvetica', 30, "bold"), activebackground='red',
                     bg='red', command=lambda:oneSelect(btn3, btn1, btn2, btn4, 'l'))
        btn3.place(x=535, y=160, anchor="s")
        btn4 = tk.Button(self, text="  Bag  ", font=('Helvetica', 30, "bold"), activebackground='red',
                     bg='red', command=lambda:oneSelect(btn4, btn1, btn3, btn2, 'b'))
        btn4.place(x=700, y=160, anchor="s")

        tk.Label(self, text="Which days?", fg='red', bg='black', font=('Helvetica', 36,
                                                                       "bold")).place(x=400, y=220, anchor="s")        
        btn5 = tk.Button(self, text="Mon", font=('Helvetica', 30, "bold"), activebackground='red',
                     bg='red', command=lambda:allSelect(btn5, 0))
        btn5.place(x=90, y=300, anchor="s")
        btn6 = tk.Button(self, text="Tue", font=('Helvetica', 30, "bold"), activebackground='red',
                     bg='red', command=lambda:allSelect(btn6, 1))
        btn6.place(x=200, y=300, anchor="s")
        btn7 = tk.Button(self, text="Wed", font=('Helvetica', 30, "bold"), activebackground='red',
                     bg='red', command=lambda:allSelect(btn7, 2))
        btn7.place(x=310, y=300, anchor="s")
        btn8 = tk.Button(self, text="Thu", font=('Helvetica', 30, "bold"), activebackground='red',
                     bg='red', command=lambda:allSelect(btn8, 3))
        btn8.place(x=420, y=300, anchor="s")
        btn9 = tk.Button(self, text="Fri", font=('Helvetica', 30, "bold"), activebackground='red',
                     bg='red', command=lambda:allSelect(btn9, 4))
        btn9.place(x=515, y=300, anchor="s")
        btn10 = tk.Button(self, text="Sat", font=('Helvetica', 30, "bold"), activebackground='red',
                     bg='red', command=lambda:allSelect(btn10, 5))
        btn10.place(x=607, y=300, anchor="s")
        btn11 = tk.Button(self, text="Sun", font=('Helvetica', 30, "bold"), activebackground='red',
                     bg='red', command=lambda:allSelect(btn11, 6))
        btn11.place(x=707, y=300, anchor="s")

        btn12 = tk.Button(self, text="Back", font=('Helvetica', 36, "bold"), activebackground='blue',
                     bg='blue', command=lambda:master.switch_frame(PageOne))
        btn12.place(x=0, y=480, anchor="sw")
        btn13 = tk.Button(self, text="Ready", font=('Helvetica', 50, "bold"), activebackground='green',
                     bg='green', command=lambda:master.switch_frame(PageEight))
        btn13.place(x=800, y=480, anchor="se")
        self.after(60000, master.switch_frame, StartPage)

#Mod or Delete Menu
class PageThree(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='black')

        tk.Label(self, text="Modify or Delete?", fg='red', bg='black', font=('Helvetica', 36,
                    "bold")).place(x=400, y=0, anchor="n")
        tk.Button(self, text="Modify RFID", font=('Helvetica', 40, "bold"), activebackground='red',
                     bg='red', command=lambda:master.switch_frame(PageSix)).place(x=400, y=230, anchor="s")
        tk.Button(self, text="Delete RFID", font=('Helvetica', 40, "bold"), activebackground='red',
                     bg='red', command=lambda:master.switch_frame(PageFive)).place(x=400, y=350, anchor="s")
        tk.Button(self, text="Back", font=('Helvetica', 36, "bold"), activebackground='blue',
                     bg='blue', command=lambda:master.switch_frame(PageOne)).place(x=0, y=480, anchor="sw")
        self.after(60000, master.switch_frame, StartPage)

#Manual Scan Menu
class PageFour(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='black')

        global scanDay
        scanDay=''

        tk.Label(self, text="Manual Scan", fg='red', bg='black', font=('Helvetica', 36,
                    "bold")).place(x=400, y=0, anchor="n")
        tk.Label(self, text="Which day?", fg='red', bg='black', font=('Helvetica', 36,
                    "bold")).place(x=400, y=220, anchor="s")        
        btn5 = tk.Button(self, text="Mon", font=('Helvetica', 30, "bold"), activebackground='red',
                     bg='red', command=lambda:oneDaySelect(btn5, btn6, btn7, btn8, btn9, btn10, btn11, 'm'))
        btn5.place(x=90, y=300, anchor="s")
        btn6 = tk.Button(self, text="Tue", font=('Helvetica', 30, "bold"), activebackground='red',
                     bg='red', command=lambda:oneDaySelect(btn6, btn5, btn7, btn8, btn9, btn10, btn11, 't'))
        btn6.place(x=200, y=300, anchor="s")
        btn7 = tk.Button(self, text="Wed", font=('Helvetica', 30, "bold"), activebackground='red',
                     bg='red', command=lambda:oneDaySelect(btn7, btn6, btn5, btn8, btn9, btn10, btn11, 'w'))
        btn7.place(x=310, y=300, anchor="s")
        btn8 = tk.Button(self, text="Thu", font=('Helvetica', 30, "bold"), activebackground='red',
                     bg='red', command=lambda:oneDaySelect(btn8, btn6, btn7, btn5, btn9, btn10, btn11, 'r'))
        btn8.place(x=420, y=300, anchor="s")
        btn9 = tk.Button(self, text="Fri", font=('Helvetica', 30, "bold"), activebackground='red',
                     bg='red', command=lambda:oneDaySelect(btn9, btn6, btn7, btn8, btn5, btn10, btn11, 'f'))
        btn9.place(x=515, y=300, anchor="s")
        btn10 = tk.Button(self, text="Sat", font=('Helvetica', 30, "bold"), activebackground='red',
                     bg='red', command=lambda:oneDaySelect(btn10, btn6, btn7, btn8, btn9, btn5, btn11, 's'))
        btn10.place(x=607, y=300, anchor="s")
        btn11 = tk.Button(self, text="Sun", font=('Helvetica', 30, "bold"), activebackground='red',
                     bg='red', command=lambda:oneDaySelect(btn11, btn6, btn7, btn8, btn9, btn10, btn5, 'n'))
        btn11.place(x=707, y=300, anchor="s")

        btn12 = tk.Button(self, text="Back", font=('Helvetica', 36, "bold"), activebackground='blue',
                     bg='blue', command=lambda:master.switch_frame(PageOne))
        btn12.place(x=0, y=480, anchor="sw")
        btn13 = tk.Button(self, text="Scan", font=('Helvetica', 50, "bold"), activebackground='green',
                     bg='green', command=lambda:scanRFID(master))
        btn13.place(x=800, y=480, anchor="se")
        self.after(60000, master.switch_frame, StartPage)

#Delete RFID Confirm Page
class PageFive(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='black')
        tk.Label(self, text="Delete RFID?", fg='red', bg='black',
                 font=('Helvetica', 32, "bold", "underline")).place(x=400, y=10, anchor="n")
        antennaPic = ImageTk.PhotoImage(Image.open("/home/pi/run/AntennaPic.jpg"))
        panel = Label(self, image=antennaPic)
        panel.image = antennaPic
        panel.place(x=400, y=70, anchor="n")
        tk.Label(self, text="Place RFID on Antenna, then hit OK", fg='red', bg='black',
                 font=('Helvetica', 32, "bold")).place(x=400, y=280, anchor="n")
        tk.Button(self, text="Back", font=('Helvetica', 36, "bold"), activebackground='blue',
                     bg='blue', command=lambda:master.switch_frame(PageThree)).place(x=0, y=480, anchor="sw")
        tk.Button(self, text="OK", font=('Helvetica', 55, "bold"), activebackground='green',
                     bg='green', command=lambda:deleteRFID(master)).place(x=800, y=480, anchor="se")
        self.after(60000, master.switch_frame, StartPage)

#Modify RFID Menu
class PageSix(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='black')

        global addDays
        addDays=list('mtwrfsn')

        tk.Label(self, text="Modify RFID?", fg='red', bg='black',
                 font=('Helvetica', 32, "bold", "underline")).place(x=400, y=10, anchor="n")

        tk.Label(self, text="Which new days?", fg='red', bg='black', font=('Helvetica', 36,
                                                                       "bold")).place(x=400, y=220, anchor="s")        
        btn5 = tk.Button(self, text="Mon", font=('Helvetica', 30, "bold"), activebackground='red',
                     bg='red', command=lambda:allSelect(btn5, 0))
        btn5.place(x=90, y=300, anchor="s")
        btn6 = tk.Button(self, text="Tue", font=('Helvetica', 30, "bold"), activebackground='red',
                     bg='red', command=lambda:allSelect(btn6, 1))
        btn6.place(x=200, y=300, anchor="s")
        btn7 = tk.Button(self, text="Wed", font=('Helvetica', 30, "bold"), activebackground='red',
                     bg='red', command=lambda:allSelect(btn7, 2))
        btn7.place(x=310, y=300, anchor="s")
        btn8 = tk.Button(self, text="Thu", font=('Helvetica', 30, "bold"), activebackground='red',
                     bg='red', command=lambda:allSelect(btn8, 3))
        btn8.place(x=420, y=300, anchor="s")
        btn9 = tk.Button(self, text="Fri", font=('Helvetica', 30, "bold"), activebackground='red',
                     bg='red', command=lambda:allSelect(btn9, 4))
        btn9.place(x=515, y=300, anchor="s")
        btn10 = tk.Button(self, text="Sat", font=('Helvetica', 30, "bold"), activebackground='red',
                     bg='red', command=lambda:allSelect(btn10, 5))
        btn10.place(x=607, y=300, anchor="s")
        btn11 = tk.Button(self, text="Sun", font=('Helvetica', 30, "bold"), activebackground='red',
                     bg='red', command=lambda:allSelect(btn11, 6))
        btn11.place(x=707, y=300, anchor="s")
        
        tk.Button(self, text="Back", font=('Helvetica', 36, "bold"), activebackground='blue',
                     bg='blue', command=lambda:master.switch_frame(PageThree)).place(x=0, y=480, anchor="sw")
        tk.Button(self, text="Ready", font=('Helvetica', 55, "bold"), activebackground='green',
                     bg='green', command=lambda:master.switch_frame(PageSeven)).place(x=800, y=480, anchor="se")
        self.after(60000, master.switch_frame, StartPage)
        
#Modify RFID Confirm page
class PageSeven(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='black')
        tk.Label(self, text="Modify RFID?", fg='red', bg='black',
                 font=('Helvetica', 32, "bold", "underline")).place(x=400, y=10, anchor="n")
        antennaPic = ImageTk.PhotoImage(Image.open("/home/pi/run/AntennaPic.jpg"))
        panel = Label(self, image=antennaPic)
        panel.image = antennaPic
        panel.place(x=400, y=70, anchor="n")
        tk.Label(self, text="Place RFID on Antenna, then hit OK", fg='red', bg='black',
                 font=('Helvetica', 32, "bold")).place(x=400, y=280, anchor="n")
        tk.Button(self, text="Back", font=('Helvetica', 36, "bold"), activebackground='blue',
                     bg='blue', command=lambda:master.switch_frame(PageSix)).place(x=0, y=480, anchor="sw")
        tk.Button(self, text="OK", font=('Helvetica', 55, "bold"), activebackground='green',
                     bg='green', command=lambda:modRFID(master)).place(x=800, y=480, anchor="se")
        self.after(60000, master.switch_frame, StartPage)

#Add RFID Confirm Page
class PageEight(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='black')
        tk.Label(self, text="Add RFID?", fg='red', bg='black',
                 font=('Helvetica', 32, "bold", "underline")).place(x=400, y=10, anchor="n")
        antennaPic = ImageTk.PhotoImage(Image.open("/home/pi/run/AntennaPic.jpg"))
        panel = Label(self, image=antennaPic)
        panel.image = antennaPic
        panel.place(x=400, y=70, anchor="n")
        tk.Label(self, text="Place RFID on Antenna, then hit OK", fg='red', bg='black',
                 font=('Helvetica', 32, "bold")).place(x=400, y=280, anchor="n")
        tk.Button(self, text="Back", font=('Helvetica', 36, "bold"), activebackground='blue',
                     bg='blue', command=lambda:master.switch_frame(PageTwo)).place(x=0, y=480, anchor="sw")
        tk.Button(self, text="OK", font=('Helvetica', 55, "bold"), activebackground='green',
                     bg='green', command=lambda:addRFID(master)).place(x=800, y=480, anchor="se")
        self.after(60000, master.switch_frame, StartPage)

#Scanning Page
class PageNine(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='black')
        global count
        count = -1

        scan = Label(self, font=('Helvetica', 64, 'bold'), fg='red', bg='black')
        scan.place(x=200, y=240, anchor="w")
        tk.Button(self, text="Cancel", font=('Helvetica', 36, "bold"), activebackground='blue',
                     bg='blue', command=lambda:master.switch_frame(PageOne)).place(x=0, y=480, anchor="sw")

        while ser.inWaiting():
            ser.read()
        
        def addDots():
            global count
            count += 1
            newtext = 'Scanning'
            for i in range(count % 4):
                newtext += '.'
            scan.config(text=newtext)
            scan.after(500, addDots)
        def respond():
            if ser.inWaiting():
                entry = ser.read()
                entry = ord(entry)
                print(entry)
                if entry < 21:
                    master.switch_frame(pageList[entry])
                    return
            self.after(1000, respond)
        addDots()
        respond()
        
#All Items Confirm Scanned Page
class PageTen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='green')
        
        tk.Label(self, text="Good to go!", fg='white', bg='green',
                 font=('Helvetica', 100, "bold")).place(x=400, y=240, anchor="c")
        tk.Button(self, text="Back", font=('Helvetica', 36, "bold"), activebackground='blue',
                     bg='blue', command=lambda:master.switch_frame(StartPage)).place(x=0, y=480, anchor="sw")

        self.after(10000, master.switch_frame, StartPage)

#RFID Added Confirm Page
class PageEleven(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='green')
        
        tk.Label(self, text="RFID Added!", fg='white', bg='green',
                 font=('Helvetica', 64, "bold")).place(x=400, y=10, anchor="n")
        tk.Label(self, text="Your new item is:", fg='white', bg='green',
                 font=('Helvetica', 36, "bold")).place(x=400, y=150, anchor="n")
        tk.Button(self, text="Back", font=('Helvetica', 36, "bold"), activebackground='blue',
                     bg='blue', command=lambda:master.switch_frame(StartPage)).place(x=0, y=480, anchor="sw")

        typePic = ImageTk.PhotoImage(Image.open("textbook.jpg"))
        panel = Label(self, image=typePic)
        panel.image = typePic
        panel.place(x=250, y=300, anchor="c")

        tk.Label(self, text="Textbook#2", fg='white', bg='green',
                 font=('Helvetica', 36, "bold")).place(x=325, y=300, anchor="w")
        
        self.after(10000, master.switch_frame, StartPage)

#RFID Modded Confirm Page
class PageTwelve(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='green')
        
        tk.Label(self, text="RFID Modded!", fg='white', bg='green',
                 font=('Helvetica', 64, "bold")).place(x=400, y=10, anchor="n")
        tk.Label(self, text="New days: M, T, W, R, F, S, N", fg='white', bg='green',
                 font=('Helvetica', 36, "bold")).place(x=400, y=150, anchor="n")
        tk.Button(self, text="Back", font=('Helvetica', 36, "bold"), activebackground='blue',
                     bg='blue', command=lambda:master.switch_frame(StartPage)).place(x=0, y=480, anchor="sw")

        typePic = ImageTk.PhotoImage(Image.open("textbook.jpg"))
        panel = Label(self, image=typePic)
        panel.image = typePic
        panel.place(x=250, y=300, anchor="c")

        tk.Label(self, text="Textbook#2", fg='white', bg='green',
                 font=('Helvetica', 36, "bold")).place(x=325, y=300, anchor="w")
        
        self.after(10000, master.switch_frame, StartPage)

#RFID Deleted Confirm Page
class PageThirteen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='white')
        
        tk.Label(self, text="RFID Deleted", fg='red', bg='white',
                 font=('Helvetica', 64, "bold")).place(x=400, y=10, anchor="n")
        tk.Label(self, text="You have deleted:", fg='black', bg='white',
                 font=('Helvetica', 36, "bold")).place(x=400, y=150, anchor="n")
        tk.Button(self, text="Back", font=('Helvetica', 36, "bold"), activebackground='blue',
                     bg='blue', command=lambda:master.switch_frame(StartPage)).place(x=0, y=480, anchor="sw")

        typePic = ImageTk.PhotoImage(Image.open("textbook.jpg"))
        panel = Label(self, image=typePic)
        panel.image = typePic
        panel.place(x=250, y=300, anchor="c")

        tk.Label(self, text="Textbook#2", fg='black', bg='white',
                 font=('Helvetica', 36, "bold")).place(x=325, y=300, anchor="w")
        
        self.after(10000, master.switch_frame, StartPage)

#Items Missed Flashing Screen
class PageFourteen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='red')

        wait = tk.Label(self, text="WAIT", fg='black', bg='red',
                 font=('Helvetica', 200, "bold"))
        wait.place(x=400, y=240, anchor="c")
        
        def blinking():
            if self['bg'] == 'red':
                self.configure(bg='white')
                wait.configure(bg='white')
            else:
                self.configure(bg='red')
                wait.configure(bg='red')
            wait.after(250, blinking)
        blinking()

        self.after(3000, master.switch_frame, PageFifteen)

#Items Missed List Screen
class PageFifteen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='white')

        wait = tk.Label(self, text="You are missing:", fg='black', bg='white',
                 font=('Helvetica',36, "bold"))
        wait.place(x=400, y=0, anchor="n")

        rfidTypeList = ["/home/pi/run/notebook.jpg", "/home/pi/run/textbook.jpg", "/home/pi/run/bag.jpg", "/home/pi/run/laptop.jpg"]
        for i in range(8):
            typeName = rfidTypeList[i%4]
            typePic = ImageTk.PhotoImage(Image.open(typeName))
            panel = Label(self, image=typePic)
            panel.image = typePic
            label = tk.Label(self, text="Textbook#8", fg='red', bg='white',
                 font=('Helvetica', 24, "bold"))
            if i%2==0:
                panel.place(x=0, y=(50 + 100*i/2), anchor="nw")
                label.place(x=110, y=(100 + 100*i/2), anchor="w")
            else:
                panel.place(x=325, y=(50 + 100*(i-1)/2), anchor="nw")
                label.place(x=435, y=(100 + 100*(i-1)/2), anchor="w")

        tk.Button(self, text="OK", font=('Helvetica', 64, "bold"), activebackground='green',
                     bg='green', command=lambda:master.switch_frame(StartPage)).place(x=800, y=480, anchor="se")

        self.after(10000, master.switch_frame, StartPage)

#RFID Added Fail Page
class PageSixteen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='white')
        
        tk.Label(self, text="RFID NOT Added!", fg='red', bg='white',
                 font=('Helvetica', 64, "bold")).place(x=400, y=110, anchor="n")
        tk.Label(self, text="Please follow instructions and try again.", fg='red', bg='white',
                 font=('Helvetica', 30, "bold")).place(x=400, y=240, anchor="c")
        tk.Button(self, text="Back", font=('Helvetica', 36, "bold"), activebackground='blue',
                     bg='blue', command=lambda:master.switch_frame(PageOne)).place(x=0, y=480, anchor="sw")
        
        self.after(10000, master.switch_frame, StartPage)

#RFID Modded Fail Page
class PageSeventeen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='white')
        
        tk.Label(self, text="RFID NOT Modded!", fg='red', bg='white',
                 font=('Helvetica', 64, "bold")).place(x=400, y=110, anchor="n")
        tk.Label(self, text="Please follow instructions and try again.", fg='red', bg='white',
                 font=('Helvetica', 30, "bold")).place(x=400, y=240, anchor="c")
        tk.Button(self, text="Back", font=('Helvetica', 36, "bold"), activebackground='blue',
                     bg='blue', command=lambda:master.switch_frame(PageOne)).place(x=0, y=480, anchor="sw")
        
        self.after(10000, master.switch_frame, StartPage)

#RFID Deleted Fail Page
class PageEighteen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='white')
        
        tk.Label(self, text="RFID NOT Deleted!", fg='red', bg='white',
                 font=('Helvetica', 64, "bold")).place(x=400, y=110, anchor="n")
        tk.Label(self, text="Please follow instructions and try again.", fg='red', bg='white',
                 font=('Helvetica', 30, "bold")).place(x=400, y=240, anchor="c")
        tk.Button(self, text="Back", font=('Helvetica', 36, "bold"), activebackground='blue',
                     bg='blue', command=lambda:master.switch_frame(PageOne)).place(x=0, y=480, anchor="sw")
        
        self.after(10000, master.switch_frame, StartPage)

#User Select Menu
class PageNineteen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='black')

        global user
        user=''

        tk.Label(self, text="Main Menu", fg='red', bg='black', font=('Helvetica', 48,
                    "bold")).place(x=400, y=0, anchor="n")
        tk.Label(self, text="Which User?", fg='red', bg='black', font=('Helvetica', 36,
                    "bold")).place(x=400, y=200, anchor="s")        
        btn5 = tk.Button(self, text="Gavin", font=('Helvetica', 46, "bold"), activebackground='red',
                     bg='red', command=lambda:oneUserSelect(master, btn5, btn6, btn7, btn8,'g'))
        btn5.place(x=20, y=300, anchor="sw")
        btn6 = tk.Button(self, text="John", font=('Helvetica', 46, "bold"), activebackground='red',
                     bg='red', command=lambda:oneUserSelect(master, btn6, btn5, btn7, btn8, 'j'))
        btn6.place(x=320, y=300, anchor="s")
        btn7 = tk.Button(self, text="Keith", font=('Helvetica', 46, "bold"), activebackground='red',
                     bg='red', command=lambda:oneUserSelect(master, btn7, btn6, btn5, btn8, 'k'))
        btn7.place(x=515, y=300, anchor="s")
        btn8 = tk.Button(self, text=" Rei ", font=('Helvetica', 46, "bold"), activebackground='red',
                     bg='red', command=lambda:oneUserSelect(master, btn8, btn6, btn7, btn5, 'r'))
        btn8.place(x=780, y=300, anchor="se")

        btn12 = tk.Button(self, text="Back", font=('Helvetica', 36, "bold"), activebackground='blue',
                     bg='blue', command=lambda:master.switch_frame(StartPage))
        btn12.place(x=0, y=480, anchor="sw")
        #btn13 = tk.Button(self, text="OK", font=('Helvetica', 50, "bold"), activebackground='green',
        #             bg='green', command=lambda:master.switch_frame(PageOne))
        #btn13.place(x=800, y=480, anchor="se")
        self.after(10000, master.switch_frame, StartPage)

#RFID List Screen
class PageTwenty(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='black')

        wait = tk.Label(self, text="List for Keith:", fg='red', bg='black',
                 font=('Helvetica',36, "bold"))
        wait.place(x=400, y=0, anchor="n")

        rfidTypeList = ["/home/pi/run/notebook.jpg", "/home/pi/run/textbook.jpg", "/home/pi/run/bag.jpg", "/home/pi/run/laptop.jpg"]
        for i in range(8):
            typeName = rfidTypeList[i%4]
            typePic = ImageTk.PhotoImage(Image.open(typeName))
            panel = Label(self, image=typePic)
            panel.image = typePic
            label = tk.Label(self, text="Textbook#8", fg='red', bg='black',
                 font=('Helvetica', 24, "bold"))
            label1 = tk.Label(self, text="M,T,W,R,F,S,N", fg='red', bg='black',
                 font=('Helvetica', 20, "bold"))
            if i%2==0:
                panel.place(x=0, y=(50 + 100*i/2), anchor="nw")
                label.place(x=110, y=(75 + 100*i/2), anchor="w")
                label1.place(x=110, y=(110 + 100*i/2), anchor="w")
            else:
                panel.place(x=325, y=(50 + 100*(i-1)/2), anchor="nw")
                label.place(x=435, y=(75 + 100*(i-1)/2), anchor="w")
                label1.place(x=435, y=(110 + 100*(i-1)/2), anchor="w")

        tk.Button(self, text="OK", font=('Helvetica', 64, "bold"), activebackground='green',
                     bg='green', command=lambda:master.switch_frame(StartPage)).place(x=800, y=480, anchor="se")

        self.after(10000, master.switch_frame, StartPage)

pageList=[StartPage,PageOne,PageTwo,PageThree,PageFour,PageFive,PageSix,PageSeven,
          PageEight,PageNine,PageTen,PageEleven,PageTwelve,PageThirteen,PageFourteen,
          PageFifteen,PageSixteen,PageSeventeen,PageEighteen,PageNineteen,PageTwenty]

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
