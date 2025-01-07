from tkinter import messagebox 
from tkinter import ttk
try:
    from SCPI import *
except:
    print("error connecting to device. is a compatible oscilloscope in HID mode connected?")
    messagebox.showerror('SCPI Error', 'Error: Could not initiate SCPI communication. Is a compatible oscilloscope in HID mode connected?')
from osciclasses import *

from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
from fftplot import plotFFT
from threading import Thread, currentThread
import os

import numpy as np


window= Tk()


window.title('SCPI Osci')

window.geometry("900x900")


#init FFT fig
fftFigure= Figure(figsize = (5, 4), 
                 dpi = 100) 

canvas= FigureCanvasTkAgg(fftFigure, master=window)
canvas.draw()
canvas.get_tk_widget().grid(column=0,row=0,rowspan=9)

liveFigure=Figure(figsize=(5,4), dpi=100)
livecanvas= FigureCanvasTkAgg(liveFigure, master=window)
livecanvas.draw()
livecanvas.get_tk_widget().grid(column=0,row=10,rowspan=9)



def plotLive(hordata,data,fig):
    fig.clf()
    p=fig.add_axes([0.1, 0.1, 0.8, 0.8])
    p.set_title("Live")
    p.plot(hordata,data)
    p.set_xlabel("s")
    p.set_ylabel("V")
    p.grid()

def plots():
    while(1):
        #getScalings()
        t=currentThread()
        if(getattr(t,"do_run", True)):
            data=scpi()
#    [1,2,2,121,21,21,21,51,234,51,51,2,21,51,51]
            x=np.multiply(list(range(len(data))),scal[0][0]*12/len(data))
            plotLive(x,np.add(np.multiply(data,scal[1]*0.64),-1.0*verOff), liveFigure)
            livecanvas.draw()

            plotFFT(data, fftFigure, xscal=scal[0][0])
            canvas.draw()

plotthread= Thread(target=plots)
plotthread.do_run=False
plotthread.start()
def startplotthread():
    try:
        scal=getScalings()
        verOff=getOffset()    
        plotthread.do_run=True
    except:
        print("error at on button action.")
    

def stopplotthread():
    plotthread.do_run=False


def sendSCPI():
    try:
        res=send(SCPIinput.get())
        print(res.tobytes().decode('utf-8'))
        SCPIresultText.set(res.tobytes().decode('utf-8'))
    except:
        print("SCPI send failed: ",SCPIinput.get())
        SCPIresultText.set("SCPI send failed: ", SCPIinput.get())

    SCPIinput.delete(0,'end')

def toggleChannelA():
    if(channelAOn)==0:
        channelAOn.set(1)
    else:
        channelAOn.set(0)
        
def toggleChannelB():
    if(channelBOn)==0:
        channelBOn.set(1)
    else:
        channelBOn.set(0)

def quitall():
    os._exit(0)

controlFrame = LabelFrame(window, text="control")
controlFrame.grid(column=1, row=0)

on_button=Button (master=controlFrame, text="Run...", command=startplotthread)
on_button.grid(column=0,row=0)
off_button=Button (master=controlFrame, text="Stop", command=stopplotthread)
off_button.grid(column=1,row=0)
exit_button = Button(master=controlFrame, text="Exit", command=quitall)
exit_button.grid(row=0, column=2)

SCPIframe = LabelFrame(window, text="SCPI")
SCPIframe.grid(column=1,row=4)

SCPIinput=Entry(master=SCPIframe)
SCPIinput.grid(column=0,row=0)
sendbutton=Button(master=SCPIframe, text="send command", command=sendSCPI)
sendbutton.grid(column=1,row=0)
SCPIresultText=StringVar()
SCPIresultLabel = Label(master=SCPIframe,textvariable=SCPIresultText)
SCPIresultLabel.grid(column=0,row=1)

channelAFrame  = LabelFrame(master=window, text="Channel 1")
channelAFrame.grid(column=1, row=1)
channelAOn=IntVar()
channelAActive = Checkbutton(master=channelAFrame, text='active',variable=channelAOn, onvalue=1, offvalue=0, command=toggleChannelA)
channelAActive.grid(column=0, row=0)
channelAOffsetLabel=Label(channelAFrame, text="Offset")
channelAOffsetLabel.grid(row=1, column=0)
channelAOffset=StringVar()
channelAOffsetBox=ttk.Combobox(channelAFrame, textvar=channelAOffset, width=25)
channelAOffsetBox.grid(row=1, column=1)
channelAScaleLabel=Label(channelAFrame, text="Scale")
channelAScaleLabel.grid(row=2, column=0)
channelAScale=StringVar()
channelAScaleBox=ttk.Combobox(channelAFrame, textvar=channelAScale, width=25)
channelAScaleBox.grid(row=2, column=1)
channelACouplingLabel=Label(channelAFrame, text="Coupling")
channelACouplingLabel.grid(row=3, column=0)
channelACoupling=StringVar()
channelACouplingBox=ttk.Combobox(channelAFrame, textvar=channelACoupling, width=25)
channelACouplingBox.grid(row=3, column=1)


channelBFrame  = LabelFrame(master=window, text="Channel 2")
channelBFrame.grid(column=1, row=2)
channelBOn=IntVar()
channelBActive = Checkbutton(master=channelBFrame, text='active',variable=channelBOn, onvalue=1, offvalue=0, command=toggleChannelA)
channelBActive.grid(column=0, row=0)
channelBOffsetLabel=Label(channelBFrame, text="Offset")
channelBOffsetLabel.grid(row=1, column=0)
channelBOffset=StringVar()
channelBOffsetBox=ttk.Combobox(channelBFrame, textvar=channelBOffset, width=25)
channelBOffsetBox.grid(row=1, column=1)
channelBScaleLabel=Label(channelBFrame, text="Scale")
channelBScaleLabel.grid(row=2, column=0)
channelBScale=StringVar()
channelBScaleBox=ttk.Combobox(channelBFrame, textvar=channelBScale, width=25)
channelBScaleBox.grid(row=2, column=1)
channelBCouplingLabel=Label(channelBFrame, text="Coupling")
channelBCouplingLabel.grid(row=3, column=0)
channelBCoupling=StringVar()
channelBCouplingBox=ttk.Combobox(channelBFrame, textvar=channelBCoupling, width=25)
channelBCouplingBox.grid(row=3, column=1)


osci=osciDevice()

try:
    scal=getScalings()
    verOff=getOffset()
except:
    errmsg='Error: Could not get scalings. Is a compatible oscilloscope in HID mode connected?'
    if os.name == 'nt':
        errmsg=errmsg+' Are you using libusb from libusb.info? If not, copy it to Windows\System32'
    print(errmsg)
    messagebox.showerror('SCPI Error', errmsg)


window.protocol('WM_DELETE_WINDOW', quitall)
window.mainloop()

