from tkinter import messagebox 
try:
    from SCPI import *
except:
    print("error connecting to device. is a compatible oscilloscope in HID mode connected?")
    messagebox.showerror('SCPI Error', 'Error: Could not initiate SCPI communication. Is a compatible oscilloscope in HID mode connected?')
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
from fftplot import plotFFT
from threading import Thread, currentThread

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
    plotthread.do_run=True


def stopplotthread():
    plotthread.do_run=False

def sendSCPI():
    try:
        res=send(SCPIinput.get())
        print(res.tobytes().decode('utf-8'))
    except:
        print("send failed: ",SCPIinput.get()) 

    SCPIinput.delete(0,'end')

on_button=Button (master=window, text="Run...", command=startplotthread)
on_button.grid(column=1,row=0)
off_button=Button (master=window, text="Stop", command=stopplotthread)
off_button.grid(column=2,row=0)

SCPIinput=Entry(master=window)
SCPIinput.grid(column=2,row=2)
sendbutton=Button(master=window, text="send", command=sendSCPI)
sendbutton.grid(column=3,row=2)

print("scalings....")

import time
#while (True):
try:
    scal=getScalings()
    verOff=getOffset()
#    time.sleep(1)
except:
    print("could not get scalings. is a compatible oscilloscope in HID mode connected?")
    messagebox.showerror('SCPI Error', 'Error: Could not get scalings. Is a compatible oscilloscope in HID mode connected?')

window.mainloop()

