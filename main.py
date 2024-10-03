from SCPI import *
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
from fftplot import plotFFT
from threading import Thread, currentThread

import numpy as np


window= Tk()

window.title('SCPI Osci')

window.geometry("700x900")


#init FFT fig
fftFigure= Figure(figsize = (5, 4), 
                 dpi = 100) 

canvas= FigureCanvasTkAgg(fftFigure, master=window)
canvas.draw()
canvas.get_tk_widget().pack()

liveFigure=Figure(figsize=(5,4), dpi=100)
livecanvas= FigureCanvasTkAgg(liveFigure, master=window)
livecanvas.draw()
livecanvas.get_tk_widget().pack()



def plotLive(hordata,data,fig):
    fig.clf()
    p=fig.add_axes([0.1, 0.1, 0.8, 0.8])
    p.set_title("Live")
    p.plot(hordata,data)
    p.grid()

def plots():
    while(1):
        #getScalings()
        t=currentThread()
        if(getattr(t,"do_run", True)):
            data=scpi()
#    [1,2,2,121,21,21,21,51,234,51,51,2,21,51,51]
            x=np.multiply(list(range(len(data))),scal*12/len(data))
            plotLive(x,data, liveFigure)
            livecanvas.draw()

            plotFFT(data, fftFigure, xscal=scal)
            canvas.draw()

plotthread= Thread(target=plots)
plotthread.do_run=False
plotthread.start()
def startplotthread():
    plotthread.do_run=True
#    plotthread.start()


def stopplotthread():
    plotthread.do_run=False

on_button=Button (master=window, text="Run...", command=startplotthread)
on_button.pack()
off_button=Button (master=window, text="Stop", command=stopplotthread)
off_button.pack()

print("scalings....")

import time
#while (True):
scal,scalStr=getScalings()
#    time.sleep(1)

window.mainloop()

